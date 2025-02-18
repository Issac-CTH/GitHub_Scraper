import time
# pip install requests
import requests
# pip install bs4
from bs4 import BeautifulSoup
# pip install mysql-connector-python
import mysql.connector

def fetch_github_trending():
    url = "https://github.com/trending?since=monthly"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # 测试访问是否成功
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，会抛出HTTPError
    except requests.exceptions.RequestException as e:
        print(f"请求错误：{e}")
        return

    # 把数据转为html类型
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # 替换为你的MySQL配置
        cnx = mysql.connector.connect(
            user='root',
            password='Msql_IssacC05418',
            host='localhost',
            database='github_trending'
        )
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
        return


    # 找出所有Box-row
    all_box = soup.find_all("article", attrs={"class": "Box-row"})
    for box in all_box:
        # 工具名字
        tool_name = box.find('a', class_='Link')['href'].strip().split('/')[-1]

        # 工具发起者
        tool_starter = box.find('span', class_="text-normal").text.strip().replace('/','')

        # 工具描述
        tool_description = box.find('p', class_="col-9 color-fg-muted my-1 pr-4").text.strip()

        # 使用的编程语言
        prog_language = box.find("span", itemprop="programmingLanguage").text.strip()

        # 总星星数
        total_star = box.find('a', class_='Link Link--muted d-inline-block mr-3').text.strip()

        # 总fork数
        total_fork = box.find('a', class_='Link Link--muted d-inline-block mr-3').find_next('a').text.strip()

        # 月星星数
        monthly_star = box.find('span', class_='d-inline-block float-sm-right').text.strip().split(' ')[0]

        # 清洗字符串数据，准备转int
        total_star = total_star.replace(',', '').strip()
        total_fork = total_fork.replace(',', '').strip()
        monthly_star = monthly_star.replace(',', '').strip()

        # 把应该是数字的数据string转int
        try:
            total_star = int(total_star)
            total_fork = int(total_fork)
            monthly_star = int(monthly_star)
        except ValueError as e:
            print(f"转换错误：{e}")
            print(f"原始数据 - 总星星：{total_star}, 总fork：{total_fork}, 月星星：{monthly_star}")
            quit(1)  # 跳过本次循环，继续处理下一个条目

        # 输出爬到的数据
        print(f"Tool Name: {tool_name}")
        print(f"Starter Name: {tool_starter}")
        print(f"Tool Description: {tool_description}")
        print(f"Programming Language: {prog_language}")
        print(f"Total Star: {total_star}")
        print(f"Total Fork: {total_fork}")
        print(f"Montly Fork: {monthly_star}")
        print("-" * 50)

        # 定义好入库参数
        query = "INSERT INTO projects (name, starter, programming_language, total_star, total_fork, monthly_star) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (tool_name, tool_starter, prog_language, total_star, total_fork, monthly_star)

        # 录入本地库
        try:
            cursor.execute(query, params)
            cnx.commit()
            print(f"成功录入数据：{tool_name}")
        except mysql.connector.Error as err:
            print(f"数据插入错误：{err}")

        # 防止访问过载被ban
        time.sleep(1)

    # 终止连接
    cnx.close()

if __name__ == "__main__":
    fetch_github_trending()