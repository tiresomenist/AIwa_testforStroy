import openai
import os

openai.api_key=os.getenv("OPENAI_API_KEY")

def completion(input):
    #빈 텍스트가 들어오는 것을 막기 위한 함수
    temp = openai.Completion.create(
        model="text-davinci-003",
        prompt=input,
        max_tokens=2048,
        temperature=0.8
    ).choices[0]
    while temp.text == "":
        temp = openai.Completion.create(
            model="text-davinci-003",
            prompt=input,
            max_tokens=2048,
            temperature=0.8
        ).choices[0]
    return temp


def storygenerator(characters, background, mood, theme, others):
    #시작 문장, 등장 인물, 분위기, 주제의식을 assistance가 아닌 prompt에 전달한 방식.
    prompt = f"Once upon a time, in a {background} far away, there were {characters}. They were in a {mood} mood. The theme of the story was {theme}."

    if others:
        prompt += f" Other details included: {others}."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": "you are a fairytale author"},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "The Characters are " + characters},
            {"role": "assistant", "content": "The background is " + background},
            {"role": "assistant", "content": "The mood is " + mood},
            {"role": "assistant", "content": "The theme is " + theme},
            {"role": "assistant", "content": f" Other details included: {others}."}
        ]
    )
    story = response.choices[0]
    return story

def fairytaleGenerator(**keyword):
    #keyword는 Characters, background, mood, theme, others
    #keyword Generator를 통해, 해당 값들이 제대로 들어오도록 코드를 구성할 것.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": "you are a fairytale author"},
            {"role": "user", "content": "First, who is the protagonist and antagonist in these keyword?"},
            {"role": "assistant", "content": "The Characters are " + keyword["characters"]},
            {"role": "assistant", "content": "The background is " + keyword["background"]},
            {"role": "assistant", "content": "The other features are " + keyword["others"]}
        ]
    )
    response2 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": "you are a fairytale author"},
            {"role": "user", "content": "second, what is the main event between protagonist and antagonist?"},
            {"role": "assistant", "content": response.choices[0].message.content},
            {"role": "assistant", "content": "The Characters are " + keyword["characters"]},
            {"role": "assistant", "content": "The background is " + keyword["background"]},
            {"role": "assistant", "content": "The mood is " + keyword["mood"]},
            {"role": "assistant", "content": "The theme is " + keyword["theme"]},
            {"role": "assistant", "content": "The other features are " + keyword["others"]}
        ]
    )

    response3 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": "you are a fairytale author"},
            {"role": "user", "content": "finally, Can you make a fairytale considering previous assistant?"},
            {"role": "assistant", "content": response.choices[0].message.content},
            {"role": "assistant", "content": response2.choices[0].message.content},
            {"role": "assistant", "content": "The Characters are " + keyword["characters"]},
            {"role": "assistant", "content": "The background is " + keyword["background"]},
            {"role": "assistant", "content": "The mood is " + keyword["mood"]},
            {"role": "assistant", "content": "The theme is " + keyword["theme"]},
            {"role": "assistant", "content": "The other features are " + keyword["others"]}
        ]
    )
    print(response3)
    print(response3.choices[0].message.content)
    return response3

def API_test(**keyword):
    #단순히 동화만 요청한 경우.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": "you are a fairytale author"},
            {"role": "user", "content": "Can you make a fairytale?"},
            {"role": "assistant", "content": "The Characters are " + keyword["characters"]},
            {"role": "assistant", "content": "The background is " + keyword["background"]},
            {"role": "assistant", "content": "The mood is " + keyword["mood"]},
            {"role": "assistant", "content": "The theme is " + keyword["theme"]},
            {"role": "assistant", "content": "The other features are " + keyword["others"]}
        ]
    )
    print(response.choices[0].message.content)
    return response


def API_test_davinci():
    #모델을 더 자주 호출 할수 있는 davinci 모델을 사용, 동화의 이야기를 순차적으로 제작.
    #잘되지않았습니다.
    responce1=completion("Create make characters of fairytale that you will create.").text.split("\n")
    #print(responce1)
    remove_set = {' ', ''}

    arr_removed = [i for i in responce1 if i not in remove_set]
    print(arr_removed)
    responce2=completion(f"Create The introduction of fairytale that you will create and The characters appear in. The characters are {arr_removed}")
    print(responce2.text)

    responce3 = completion(f"Create Second Scene of fairytale which have 7-Scene that you will create and The characters appear in. The previous Scene is {responce2.text}. The characters are {arr_removed}")
    print(responce3)
    responce4 = completion(f"create Ending of fairytale. that you will create and The characters appear in. The characters are {arr_removed}")
    print(responce4)


if __name__ == '__main__':
    #현재 제일 성능 좋은 것은 storygenerator로 생각됩니다.
    print(storygenerator(characters="princess, queen, rabbit, cat, prince",
                        background="The Middle Ages",
                        mood="Fantastic, dreamy",
                        theme="Goodwill and Punishment",
                        others="the queen is villain").message.content)
    #API_test_davinci()
    # API_test(characters="princess, queen, rabbit, cat, prince",
    #                    background="The Middle Ages",
    #                    mood="Fantastic, dreamy",
    #                    theme="Goodwill and Punishment",
    #                    others="the queen is villain")
    # time.sleep(100)
    # fairytaleGenerator(characters="princess, queen, rabbit, cat, prince",
    #                    background="The Middle Ages",
    #                    mood="Fantastic, dreamy",
    #                    theme="Goodwill and Punishment",
    #                    others="the queen is villain")
