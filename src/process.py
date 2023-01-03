import argparse

from crawler import InstaUserKnow, InstaCrawler


def usage():
    return """
        python3 process.py [tag]
    """


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instagram Crawler", usage=usage())
    
    parser.add_argument("-id", "--insta_id", help="instagram id")
    parser.add_argument("-pw", "--insta_pw", help="instagram pw")
    parser.add_argument( "-n", '--number', type=int, default=100, help="number of follower list")
    
    args = parser.parse_args()

    _userknow = InstaUserKnow()
    _crawler = InstaCrawler(args.insta_id, args.insta_pw, args.number)

    crawl_user_list = _userknow.get_insta_user_list()
    
    driver = _crawler.execute_chromedriver()
    request_session = _crawler.login_insta(driver)
    for userid in crawl_user_list:
        _crawler.crawl_follwer_list(request_session, userid)
        _crawler.execute_sleep(60, 60*30)