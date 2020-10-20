import requests


def issue_topic(letter,exclude,challenge,step,swap):
    '''
    利用相应网络接口发布题目
    填写字段:letter,exclude,challenge,step,swap
    '''
    url = "http://47.102.118.1:8089/api/challenge/create"
    title = {
        "teamid":52 ,
        "data": {
            "letter": letter,
            "exclude": exclude,
            "challenge": challenge,
            "step": step,
            "swap": swap
        },
        "token": "3585feb4-f430-4e99-b80d-99f952c41798"
    }

    r = requests.post(url,json=title)
    print(r.text)


if __name__ == "__main__":
    letter = "M"
    exclude = 9
    challenge = [
                [1, 7, 3],
                [0, 6, 8],
                [5, 4, 2]
            ]
    step = 15
    swap = [2,7]
    issue_topic(letter, exclude, challenge, step, swap)