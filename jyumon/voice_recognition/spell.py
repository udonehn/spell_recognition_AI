import os
from openai import OpenAI

api_key = ''

system_message = """
You are an AI that scores between 0 and 100 depending on the strength of the order.

If the user gives you an order, score it.

However, you have to meet the criteria below.

1. Base score is 0, no ceiling for score
2. when ファイア is detected 500 points added.
3. when ボール is detected 200 points added.
4. when ストーム is detected 400 points added.
5. when ウォール is detected 300 points added.
6. when スピア are detected 350 points added.
7. when ハンマー is detected 450 points added. 
8. when アイス is detected 250 points added. 
9. when ライトニング is detected 550 points added.
10. when ブレイク is detected 600 points added.
11. when インパクト is detected 500 points added.
12. when ブースト is detected 700 points added.
13. when サンダー is detected 650 points added. 

Also, score each Japanese letter and add more.

あ:80点, い:75点, う:90点, え:70点, お:85点, か:80点, が(濁音):90点, き:85点, ぎ(濁音):95点, く:90点, ぐ(濁音):95点, け:75点, げ(濁音):85点, こ:85点, ご(濁音):90点, さ:70点, ざ(濁音):85点, し:90点, じ(濁音):95点, す:80点, ず(濁音):90点, せ:75点, ぜ(濁音):85点, そ:70点, ぞ(濁音):85点, た:90点, だ(濁音):95点, ち:95点, ぢ(濁音):90点, つ:90点, づ(濁音):95点, て:85点, で(濁音):90点, と:90点, ど(濁音):95点, な:75点, に:70点, ぬ:80点, ね:75点, の:80点, は(半濁音):85点, ば(濁音):90点, ぱ(半濁音):80点, ひ:75点, び(濁音):90点, ぴ(半濁音):85点, ふ(半濁音):80点, ぶ(濁音):90点, ぷ(半濁音):85点, へ:70点, べ(濁音):85点, ぺ(半濁音):80点, ほ(半濁音):85点, ぼ(濁音):90点, ぽ(半濁音):85点, ま:90点, み:70点, む:85点, め:75点, も:90点, や:80点, ゆ:75点, よ:85点, ら:90点, り:85点, る:80点, れ:75点, ろ:80点, わ:75点, を:70点, ん:95点, ー:95点
You don't have to score small letters (捨て仮) like ぁ, ぃ, ぅ, ぇ, ぉ, っ, ゃ, ゅ, ょ.


If your order does not meet the above criteria, don't add your score arbitrarily.

Print out the score, and let me know why in the lower line.

Print out the results in the format as below. No further explanation is needed. :

example 1(in the case of ファイアボール):
700
500 points more related to ファイア, 200 points more related to ボール. You finally get 700 points.

example 2(in the case of エクスプロージョン):
500
500 points more related to ファイア. You finally get 500 points.


example 3(in the case of 黒棺(くろひつぎ)):
0
No score that meets the criteria. You finally get 0 points.

example 3(in the case of サンダースピア):
1000
650 points more related to サンダー, 350 points more related to スピア. You finally get 1000 points.
"""



"""
If your order does not meet the above criteria, add your score arbitrarily.
If your order doesn't meet the above criteria, don't add your score arbitrarily.
"""



client = OpenAI(api_key=api_key)

extra_scores_dict = {
    "あ": 80, "い": 75, "う": 90, "え": 70, "お": 85,
    "か": 80, "が": 90, "き": 85, "ぎ": 95, "く": 90,
    "ぐ": 95, "け": 75, "げ": 85, "こ": 85, "ご": 90,
    "さ": 70, "ざ": 85, "し": 90, "じ": 95, "す": 80,
    "ず": 90, "せ": 75, "ぜ": 85, "そ": 70, "ぞ": 85,
    "た": 90, "だ": 95, "ち": 95, "ぢ": 90, "つ": 90,
    "づ": 95, "て": 85, "で": 90, "と": 90, "ど": 95,
    "な": 75, "に": 70, "ぬ": 80, "ね": 75, "の": 80,
    "は": 85, "ば": 90, "ぱ": 80, "ひ": 75, "び": 90,
    "ぴ": 85, "ふ": 80, "ぶ": 90, "ぷ": 85, "へ": 70,
    "べ": 85, "ぺ": 80, "ほ": 85, "ぼ": 90, "ぽ": 85,
    "ま": 90, "み": 70, "む": 85, "め": 75, "も": 90,
    "や": 80, "ゆ": 75, "よ": 85, "ら": 90, "り": 85,
    "る": 80, "れ": 75, "ろ": 80, "わ": 75, "を": 70,
    "ん": 95, "ー": 95,
    "ア": 80, "イ": 75, "ウ": 90, "エ": 70, "オ": 85,
    "カ": 80, "ガ": 90, "キ": 85, "ギ": 95, "ク": 90,
    "グ": 95, "ケ": 75, "ゲ": 85, "コ": 85, "ゴ": 90,
    "サ": 70, "ザ": 85, "シ": 90, "ジ": 95, "ス": 80,
    "ズ": 90, "セ": 75, "ゼ": 85, "ソ": 70, "ゾ": 85,
    "タ": 90, "ダ": 95, "チ": 95, "ヂ": 90, "ツ": 90,
    "ヅ": 95, "テ": 85, "デ": 90, "ト": 90, "ド": 95,
    "ナ": 75, "ニ": 70, "ヌ": 80, "ネ": 75, "ノ": 80,
    "ハ": 85, "バ": 90, "パ": 80, "ヒ": 75, "ビ": 90,
    "ピ": 85, "フ": 80, "ブ": 90, "プ": 85, "ヘ": 70,
    "ベ": 85, "ペ": 80, "ホ": 85, "ボ": 90, "ポ": 85,
    "マ": 90, "ミ": 70, "ム": 85, "メ": 75, "モ": 90,
    "ヤ": 80, "ユ": 75, "ヨ": 85, "ラ": 90, "リ": 85,
    "ル": 80, "レ": 75, "ロ": 80, "ワ": 75, "ヲ": 70,
    "ン": 95, "ー": 95
}



def call_gpt(prompt, model="gpt-3.5-turbo-0125", max_tokens=150, temperature=0.7, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    return response


def get_score(spell):
    # example
    dialogue = call_gpt(spell)
    score, reason = dialogue.choices[0].message.content.split("\n")
    print("score(by criteria): " + score)
    print("reason: " + reason)

    extra_score = get_extra_score(spell)
    print("extra score: " + str(extra_score))

    # print the total tokens used
    total_tokens = dialogue.usage.total_tokens
    print(f"Total tokens used: {total_tokens}")

    # print(dialogue.choices)

    total_score = int(score) + extra_score
    print("total score: " + str(total_score))
    return total_score


def get_extra_score(spell):
    extra_points = 0
    for letter in spell:
        if letter in extra_scores_dict:
            print(f"{letter}: {extra_scores_dict[letter]}")
            extra_points += extra_scores_dict[letter]
    return extra_points


# spell = "アイシクルランス"
# print(get_score(spell))
