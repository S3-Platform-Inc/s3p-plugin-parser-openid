import dateparser
import datetime
import time
import re
from s3p_sdk.plugin.payloads.parsers import S3PParserBase
from s3p_sdk.types import S3PRefer, S3PDocument, S3PPlugin
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class OpenID(S3PParserBase):
    """
    A Parser payload that uses S3P Parser base class.
    """
    HOST = 'https://openid.net/specs/?C=M;O=D'

    def __init__(self, refer: S3PRefer, plugin: S3PPlugin, web_driver: WebDriver, max_count_documents: int = None,
                 last_document: S3PDocument = None):
        super().__init__(refer, plugin, max_count_documents, last_document)

        # Тут должны быть инициализированы свойства, характерные для этого парсера. Например: WebDriver
        self._driver = web_driver
        self._wait = WebDriverWait(self._driver, timeout=20)

    def _parse(self):
        """
        Метод, занимающийся парсингом. Он добавляет в _content_document документы, которые получилось обработать
        :return:
        :rtype:
        """
        # HOST - это главная ссылка на источник, по которому будет "бегать" парсер
        self.logger.debug(F"Parser enter to {self.HOST}")

        # ========================================
        # Тут должен находится блок кода, отвечающий за парсинг конкретного источника
        # -
        self._driver.get(self.HOST)

        pattern_ignore_drafts = r'^(?!.*-\d+\.html$).*\.html$'

        specs = self._driver.find_elements(By.XPATH, '//a[contains(text(),\'.html\')]')
        raw_web_links = [spec.get_attribute('href') for spec in specs]
        web_links = [url for url in raw_web_links if re.match(pattern_ignore_drafts, url)]
        for web_link in web_links:
            self._driver.get(web_link)
            if len(self._driver.find_elements(By.XPATH, '//h2[text() = \'Renamed Specification\']')) > 0:
                self.logger.debug('Waiting redirect')
                time.sleep(7)
            time.sleep(2)

            try:
                title = self._driver.find_element(By.ID, 'title').text
            except:
                title = self._driver.find_element(By.TAG_NAME, 'h1').text

            try:
                pub_date = dateparser.parse(self._driver.find_element(By.TAG_NAME, 'time').text)
            except:
                pub_date = dateparser.parse(
                    self._driver.find_elements(By.XPATH, '//table[not(@class = \'TOCbug\')][1]/tbody/tr/td')[-1].text)

            try:
                abstract = self._driver.find_element(By.ID, 'section-abstract').text
            except:
                abstract = None

            text_content = self._driver.find_element(By.TAG_NAME, 'body').text

            try:
                workgroup = self._driver.find_element(By.CLASS_NAME, 'workgroup').text
            except:
                workgroup = None

            try:
                authors = []
                author_struct = self._driver.find_elements(By.CLASS_NAME, 'author')
                for author in author_struct:
                    authors.append({'name': author.find_element(By.CLASS_NAME, 'author-name').text,
                                    'org': author.find_element(By.CLASS_NAME, 'org').text})
            except:
                authors = [x.text for x in
                           self._driver.find_elements(By.XPATH, '//table[not(@class = \'TOCbug\')][1]/tbody/tr/td')]

            other_data = {'workgroup': workgroup,
                          'authors': authors}

            doc = S3PDocument(None,
                              title,
                              abstract,
                              text_content,
                              web_link,
                              None,
                              other_data,
                              pub_date,
                              datetime.datetime.now())

            self._find(doc)

        # ---
        # ========================================
        ...
