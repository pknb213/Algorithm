"""
신규 아이디 추천
카카오에 입사한 신입 개발자 네오는 카카오계정개발팀에 배치되어,
카카오 서비스에 가입하는 유저들의 아이디를 생성하는 업무를 담당하게 되었습니다.
네오에게 주어진 첫 업무는 새로 가입하는 유저들이 카카오 아이디 규칙에 맞지 않는 아이디를 입력했을 때,
입력된 아이디와 유사하면서 규칙에 맞는 아이디를 추천해주는 프로그램을 개발하는 것입니다.
다음은 카카오 아이디의 규칙입니다.

아이디의 길이는 3자 이상 15자 이하여야 합니다.
아이디는 알파벳 소문자, 숫자, 빼기(-), 밑줄(_), 마침표(.) 문자만 사용할 수 있습니다.
단, 마침표(.)는 처음과 끝에 사용할 수 없으며 또한 연속으로 사용할 수 없습니다.
네오는 다음과 같이 7단계의 순차적인 처리 과정을 통해 신규 유저가 입력한 아이디가 카카오 아이디 규칙에 맞는 지 검사하고
규칙에 맞지 않은 경우 규칙에 맞는 새로운 아이디를 추천해 주려고 합니다.
신규 유저가 입력한 아이디가 new_id 라고 한다면,

1단계 new_id의 모든 대문자를 대응되는 소문자로 치환합니다.
2단계 new_id에서 알파벳 소문자, 숫자, 빼기(-), 밑줄(_), 마침표(.)를 제외한 모든 문자를 제거합니다.
3단계 new_id에서 마침표(.)가 2번 이상 연속된 부분을 하나의 마침표(.)로 치환합니다.
4단계 new_id에서 마침표(.)가 처음이나 끝에 위치한다면 제거합니다.
5단계 new_id가 빈 문자열이라면, new_id에 "a"를 대입합니다.
6단계 new_id의 길이가 16자 이상이면, new_id의 첫 15개의 문자를 제외한 나머지 문자들을 모두 제거합니다.
     만약 제거 후 마침표(.)가 new_id의 끝에 위치한다면 끝에 위치한 마침표(.) 문자를 제거합니다.
7단계 new_id의 길이가 2자 이하라면, new_id의 마지막 문자를 new_id의 길이가 3이 될 때까지 반복해서 끝에 붙입니다.
예를 들어, new_id 값이 ...!@BaT#*..y.abcdefghijklm 라면, 위 7단계를 거치고 나면 new_id는 아래와 같이 변경됩니다.

1단계 대문자 'B'와 'T'가 소문자 'b'와 't'로 바뀌었습니다.
"...!@BaT#*..y.abcdefghijklm" → "...!@bat#*..y.abcdefghijklm"

2단계 '!', '@', '#', '*' 문자가 제거되었습니다.
"...!@bat#*..y.abcdefghijklm" → "...bat..y.abcdefghijklm"

3단계 '...'와 '..' 가 '.'로 바뀌었습니다.
"...bat..y.abcdefghijklm" → ".bat.y.abcdefghijklm"

4단계 아이디의 처음에 위치한 '.'가 제거되었습니다.
".bat.y.abcdefghijklm" → "bat.y.abcdefghijklm"

5단계 아이디가 빈 문자열이 아니므로 변화가 없습니다.
"bat.y.abcdefghijklm" → "bat.y.abcdefghijklm"

6단계 아이디의 길이가 16자 이상이므로, 처음 15자를 제외한 나머지 문자들이 제거되었습니다.
"bat.y.abcdefghijklm" → "bat.y.abcdefghi"

7단계 아이디의 길이가 2자 이하가 아니므로 변화가 없습니다.
"bat.y.abcdefghi" → "bat.y.abcdefghi"

따라서 신규 유저가 입력한 new_id가 ...!@BaT#*..y.abcdefghijklm일 때, 네오의 프로그램이 추천하는 새로운 아이디는 bat.y.abcdefghi 입니다.

[문제]
신규 유저가 입력한 아이디를 나타내는 new_id가 매개변수로 주어질 때, 네오가 설계한 7단계의 처리 과정을 거친 후의 추천 아이디를 return 하도록 solution 함수를 완성해 주세요.

[제한사항]
new_id는 길이 1 이상 1,000 이하인 문자열입니다.
new_id는 알파벳 대문자, 알파벳 소문자, 숫자, 특수문자로 구성되어 있습니다.
new_id에 나타날 수 있는 특수문자는 -_.~!@#$%^&*()=+[{]}:?,<>/ 로 한정됩니다.

[입출력 예]
no	                new_id	                            result
예1	    "...!@BaT#*..y.abcdefghijklm"           	"bat.y.abcdefghi"
예2             	"z-+.^."                           	"z--"
예3              	"=.="	                             "aaa"
예4	              "123_.def"	                      "123_.def"
예5        	"abcdefghijklmn.p"	                    "abcdefghijklmn"
입출력 예에 대한 설명
입출력 예 #1
문제의 예시와 같습니다.

입출력 예 #2
7단계를 거치는 동안 new_id가 변화하는 과정은 아래와 같습니다.

1단계 변화 없습니다.
2단계 "z-+.^." → "z-.."
3단계 "z-.." → "z-."
4단계 "z-." → "z-"
5단계 변화 없습니다.
6단계 변화 없습니다.
7단계 "z-" → "z--"

입출력 예 #3
7단계를 거치는 동안 new_id가 변화하는 과정은 아래와 같습니다.

1단계 변화 없습니다.
2단계 "=.=" → "."
3단계 변화 없습니다.
4단계 "." → "" (new_id가 빈 문자열이 되었습니다.)
5단계 "" → "a"
6단계 변화 없습니다.
7단계 "a" → "aaa"

입출력 예 #4
1단계에서 7단계까지 거치는 동안 new_id(123_.def)는 변하지 않습니다. 즉, new_id가 처음부터 카카오의 아이디 규칙에 맞습니다.

입출력 예 #5
1단계 변화 없습니다.
2단계 변화 없습니다.
3단계 변화 없습니다.
4단계 변화 없습니다.
5단계 변화 없습니다.
6단계 "abcdefghijklmn.p" → "abcdefghijklmn." → "abcdefghijklmn"
7단계 변화 없습니다.

"""
from datetime import timedelta
from timeit import default_timer as timer
import string
import re

def solution(_new_id):
    st = timer()
    # new_id = ".Aa\tBb0 12..3+-_!@# ."
    new_id = _new_id.lower()
    # print("1 >", timedelta(seconds=timer() - st), new_id)
    new_id = "".join(re.findall(r'\w|[-_.]', new_id))
    # print("2 >", timedelta(seconds=timer() - st), new_id)

    new_id = ".".join(re.findall('[^..]+', new_id))
    # print("3 >", timedelta(seconds=timer() - st), new_id)

    new_id = new_id.strip('.')
    # print("4 >", timedelta(seconds=timer() - st), new_id)

    if not len(new_id):
        new_id = "a"
    # print("5 >", timedelta(seconds=timer() - st), new_id)

    new_id = new_id[:15].strip('.')
    # print("6 >", timedelta(seconds=timer() - st), new_id)

    if len(new_id) < 3:
        arr = [new_id]
        while len(new_id) < 3:
            arr.append(new_id[-1])
            new_id = "".join(arr)
        new_id = new_id[:3]
    # print("7 >", timedelta(seconds=timer() - st), new_id)

    # print(new_id)
    return new_id


def soltion2(new_id):
    st = timer()
    id1 = new_id.lower()
    # print("1 >", timedelta(seconds=timer() - st))

    step2_filter = string.digits + string.ascii_lowercase + '-_.'
    id2 = ''
    for c in id1:
        if c in step2_filter: id2 += c
    # print("2 >", timedelta(seconds=timer() - st))

    id3 = ''
    for c in id2:
        if c != '.':
            id3 += c
        else:
            if id3 and id3[-1] == '.': continue
            id3 += c
    # print("3 >", timedelta(seconds=timer() - st))

    id4 = id3.strip('.')
    # print("4 >", timedelta(seconds=timer() - st))

    id5 = id4[:]
    if not id5: id5 = 'a'
    # print("5 >", timedelta(seconds=timer() - st))

    id6 = id5[:15]
    if id6[-1] == '.': id6 = id6[:-1]
    # print("6 >", timedelta(seconds=timer() - st))

    id7 = id6[:]
    while len(id7) < 3: id7 = id7 + id7[-1]
    # print("7 >", timedelta(seconds=timer() - st))
    return id7


def solution3(_new_id):
    # new_id = ".Aa\tBb0 12..3+-_!@# ."
    str1 = _new_id.lower()
    str2 = "".join(re.findall('\w|[-_.]', str1))
    str3 = ".".join(re.findall('[^..]+', str2))
    str4 = str3.strip('.')
    str5 = str4
    if not len(str5):
        str5 = "a"
    str6 = str5[:15].strip('.')
    str7 = str6
    if len(str7) < 3:
        arr = [str7]
        while len(str7) < 3:
            arr.append(str7[-1])
            str7 = "".join(arr)
        return str7[:3]
    return str7


def solution4(_new_id):
    # new_id = ".Aa\tBb0 12..3+-_!@# ."
    str1 = _new_id.lower()
    str2 = "".join(re.findall('\w|[-_.]', str1))
    # Test Case 4, 14, 16, 17, 20, 21, 25번 에러 모두 여기서 발생
    # 원인 : 한번만 replace 하기 때문에 .... 경우 .. 다시 점 두개가 발생하는데 냅둬서 에러
    # 방안 : 루프를 돌려서 계속 ..일 때마다 .으로 줄여나가기
    # 해결 : 정규표현식으로 ..* 는 일괄 .으로 수정 => 성공
    str3 = ''
    for c in str2:
        if c != '.':
            str3 += c
        else:
            if str3 and str3[-1] == '.': continue
            str3 += c
    str4 = str3.strip('.')
    str5 = str4
    if not len(str5):
        str5 = "a"
    str6 = str5[:15].strip('.')
    str7 = str6
    if len(str7) < 3:
        arr = [str7]
        while len(str7) < 3:
            arr.append(str7[-1])
            str7 = "".join(arr)
        return str7[:3]
    return str7


def solution5(new_id):
    st = new_id
    st = st.lower()
    st = re.sub('[^a-z0-9\-_.]', '', st)
    st = re.sub('\.+', '.', st)
    st = re.sub('^[.]|[.]$', '', st)
    st = 'a' if len(st) == 0 else st[:15]
    st = re.sub('^[.]|[.]$', '', st)
    st = st if len(st) > 2 else st + "".join([st[-1] for i in range(3-len(st))])
    return st


st = timer()
print("\n", solution("...!@BaT#...*..y.abcdefghijklm"))
# Test Cases : 4, 14, 16, 17, 20, 21, 25
print(timedelta(seconds=timer() - st))

st = timer()
print("\n", soltion2("...!@BaT#...*..y.abcdefghijklm"))
# Test Cases : Success
print(timedelta(seconds=timer() - st))

st = timer()
print("\n", solution3("...!@BaT#...*..y.abcdefghijklm"))
# Test Cases : 4, 14, 16, 17, 20, 21, 25
print(timedelta(seconds=timer() - st))

st = timer()
print("\n", solution4("...!@BaT#...*..y.abcdefghijklm"))
# Test Cases :
print(timedelta(seconds=timer() - st))

st = timer()
print("\n", solution5("...!@BaT#...*..y.abcdefghijklm"))
# Test Cases :
print(timedelta(seconds=timer() - st))