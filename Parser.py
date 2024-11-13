import os 
import time
from bs4 import BeautifulSoup
import requests

#TODO: перенести куданить
SELENIUM_BINARY_PATH = f"{os.getcwd()}\\Parser\\Browser\\chrome.exe"
SELENIUM_EXECUTABLE_PATH = f"{os.getcwd()}\\Parser\\Browser\\chromedriver.exe"



class Parser:
    #я хз че тут инитить если честно. Пусть пока будет на классметодах 


    class Site:
        '''
        Класс отвечающий за парсинг определенных сайтов. 
        '''
        class thatpervert():
            '''
            Подкласс для парсинга thatpervert.com
            '''
            @classmethod
            def by_tag(self, tag:str, page = None, driver = None, parse_timeout = 5):
                try:
                    '''
                    Получение всех постов на странице. 
                    Принимает:
                    -tag : str - тег поиска
                    -page : int/str - страница/страницы.
                    -driver - selenium драйвер. Если None, создается новый.
                    -parse_timeout - таймаут при парсинге. 
                    --Итогом формируется страница  thatpervert.com/tag/TAG/PAGE

                    Возвращает: список с путями до файлов. 
                    '''
                    #Запуск драйвера если не передан
                    if driver is None:
                        driver = Parser._init_selenium(SELENIUM_BINARY_PATH, SELENIUM_EXECUTABLE_PATH)
                
                    from selenium.webdriver.common.by import By
                    #Формирование страницы для дальнейшей работы
                    base_url = "thatpervert.com"

                    #обработка page для вычисления случайной страницы 
                    if page is None:
                        driver.get(f"https://{base_url}/tag/{tag}")
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        #достаем номер максимальной страницы.
                        for href in soup.findAll("a", class_="next"):
                            max_page = href['href']
                        max_page = int(max_page.split("/")[-1])
                        import random
                        work_page = random.randint(0,max_page)
                        work_url = f"https://{base_url}/tag/{tag}/{str(work_page)}"
                        print(max_page)
                        print(work_page)
                    else:
                        work_url = f"https://{base_url}/tag/{tag}/{str(page)}"

                    #Обработка страницы. Получение контейнеров. 
                    driver.get(work_url)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    containers = soup.findAll("div", class_="postContainer")

                    parsedData = []

                    #обработка контейнеров постов.
                    for container in containers:
                        #Получение данных поста.
                        content = container.find("div", class_="post_content")

                        #Получение линков. Картинок и видео
                        ImagesLinks =  content.findAll("img")
                        VideoLinks = content.findAll("span", class_ = "video_holder")
                    
                        #НЕ РАБОТАЕТ! ПРОПУСКАЕТМСЯ 
                        if len(VideoLinks) != 0:
                            continue
                            for index, Video in enumerate(VideoLinks):
                                time.sleep(timeout) #timeout
                                Video = Video.find("source")
                                if Video['type'] == "video/webm":
                                    VideoUrl = "https:" +Video['src']
                                    print(f"Get video: {VideoUrl}")
                                    Sel_Driver.get(VideoUrl)
                                    image_element = Sel_Driver.find_element(By.TAG_NAME, 'video')
                                    scr = image_element.screenshot_as_png
                                    full_unique_name = f"{unique_tag_name}_{unique_queue_id}_{unique_container_id}_{index}.webm"
                                    with open(f"{os.getcwd()}/Content/{full_unique_name}", 'wb') as f:
                                        f.write(scr)
                                    #Data.add_data("thatpervert", full_unique_name)

                        #Получение изображений (если они есть)
                        images = []
                        if len(ImagesLinks) != 0:
                            for index, link in enumerate(ImagesLinks):
                                time.sleep(parse_timeout) #Таймаут перед запросом
                                #Получение url изображения
                                ImageUrl = "https:" + link['src']
                                #Получение тегов. Их можно достать из альта изображения
                                ImageTags = link['alt']
                                print(f"Get photo {index}")
                                pre_name = "-".join([str(element) for element in (ImageUrl.split('/')[-1]).split("-")][0:-1])
                                full_unique_path = f"{os.getcwd()}/Content/{pre_name}_{index}.png"
                                if os.path.exists(full_unique_path):
                                    print("file already exists")
                                    continue
                                #Так как качество и так говно, дополнительно прогоняем через сессию.
                                #так как летит 403, берем все хедеры прямиком из сессии браузера. Это позволяет обойти защиту. 
                                cookies = driver.get_cookies()
                                session = requests.Session()
                                for cookie in cookies:
                                   session.cookies.set(cookie['name'], cookie['value'])
                                headers = {
                                    'User-Agent': driver.execute_script("return navigator.userAgent;"),
                                    'Referer': driver.current_url,
                                }
                                response = session.get(ImageUrl, headers=headers)


                                #driver.get(ImageUrl)
                                #image_element = driver.find_element(By.TAG_NAME, 'img')
                                #scr = image_element.screenshot_as_png

                                print (full_unique_path)
                                with open(f"{full_unique_path}", 'wb') as f:
                                    f.write(response.content)
                                    images.append(f"{full_unique_path}")


                                #with open(f"{full_unique_path}", 'wb') as f:
                                #    f.write(scr)
                                #    images.append(f"{full_unique_path}")

                        images.insert(0, ImageTags)
                        parsedData.append(images)
                    Parser._kill_selenium(driver)
                    return parsedData
                except Exception as exception:
                    print(str(exception))
                    return False

                    



    @staticmethod
    def _init_selenium(binaryPath, executablePath):
        '''
        Инициализация драйвера для работы 
        ''' 
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service  
        options = webdriver.ChromeOptions()
        WINDOW_SIZE = "1920,1080"
        options.add_argument("--headless")
        options.add_argument("--window-size=%s" % WINDOW_SIZE)
        #options.headless = True не работает
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--no-sandbox")
        options.add_experimental_option("detach", True)
        options.binary_location = binaryPath
        SeleniumDriver = webdriver.Chrome(service=Service(executable_path=executablePath), options=options)
        return SeleniumDriver

    @staticmethod
    def _kill_selenium(SeleniumDriver):
        '''
        Мягкое завершение работы драйвера selenium
        '''
        try:
            SeleniumDriver.quit()
            return True
        except Exception as exception:
            print(str(exception)) #добавить логирование 
            return False
