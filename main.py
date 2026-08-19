import json

DEFAULT_QUIZ = [
  {
    "id": 1,
    "question": "파이썬에서 리스트의 마지막 요소에 접근하는 올바른 코드는 무엇인가?",
    "choices": [
      "numbers[0]",
      "numbers[-1]",
      "numbers[last]",
      "numbers.end()"
    ],
    "answer": 2
  },
  {
    "id": 2,
    "question": "파이썬에서 함수를 정의할 때 사용하는 키워드는 무엇인가?",
    "choices": [
      "function",
      "func",
      "define",
      "def"
    ],
    "answer": 4
  },
  {
    "id": 3,
    "question": "다음 코드의 실행 결과는 무엇인가?\n\nnumbers = [1, 2, 3]\nnumbers.append(4)\nprint(numbers)",
    "choices": [
      "[1, 2, 3]",
      "[1, 2, 3, 4]",
      "[4, 1, 2, 3]",
      "[1, 2, 3, [4]]"
    ],
    "answer": 2
  },
  {
    "id": 4,
    "question": "파이썬 딕셔너리에서 키 'name'에 해당하는 값을 가져오는 올바른 코드는 무엇인가?",
    "choices": [
      "user['name']",
      "user.name",
      "user(name)",
      "user->name"
    ],
    "answer": 1
  },
  {
    "id": 5,
    "question": "다음 코드의 실행 결과는 무엇인가?\n\nfor number in range(3):\n    print(number)",
    "choices": [
      "1, 2, 3이 차례로 출력된다.",
      "0, 1, 2가 차례로 출력된다.",
      "0, 1, 2, 3이 차례로 출력된다.",
      "3만 출력된다."
    ],
    "answer": 2
  }
]

QUIZ_DATA_FILE = "quiz.json"
STATE_FILE = "state.json"
SYS = "[SYSTEM]"

def print2():
    print("=" * 80)


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


"""
반드시 클래스여야 하는가는 아래 기준으로 판단했음.
- 함께 유지해야 할 상태가 있는가?
- 그 상태를 다루는 동작이 여러 개 있는가?

1. 퀴즈 진행: 아래 클래스들을 오케스트레이션 -> QuizGame
2. 퀴즈 생성과 출제: 퀴즈 문제 출력 / 정답과 사용자의 답 비교 -> Quiz
3. 퀴즈 목록 관리: 퀴즈 문항 추가 / 퀴즈 목록 보여주기 -> QuizManager
4. 점수 관리: 퀴즈 풀이 후 점수 반영 / 점수 통보 / 최고 점수 기록 및 갱신 -> ScoreManager
"""

class QuizGame:
    def __init__(self, quiz_manager, score_manager):
        self.quiz_manager = quiz_manager
        self.score_manager = score_manager

    def start(self):
        self.score_manager.reset()

        for quiz in self.quiz_manager.get_all():
            quiz.display()
            user_answer = self.get_user_answer()

            is_correct = quiz.is_correct(user_answer)
            self.score_manager.record(is_correct)

        self.show_result()



class Quiz:
    def __init__(self, id, question, choices, answer):
        self.quiz_id = id
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(f"{self.quiz_id}. {self.question}")

        for num, choice in enumerate(self.choices, 1):
            print(f"   ({num}) {choice}")
        print()

    def is_correct(self, user_answer):
        return self.answer == user_answer


"""
오류를 발견하는 책임과 사용자에게 대응 방법을 결정하는 책임을 분리
"""
def main():
    # 퀴즈 데이터와 점수 데이터 불러오기
    try:
        quizzes = load_json(QUIZ_DATA_FILE)
    except FileNotFoundError:
        print(f"{SYS} 퀴즈 파일을 찾을 수 없어 기본 퀴즈로 대체합니다.")
        quizzes = DEFAULT_QUIZ

    try:    
        state = load_json(STATE_FILE)
    except FileNotFoundError:
        print(f"{SYS} 파일을 찾을 수 없습니다.")

    except json.JSONDecodeError:
        print(f"{SYS} data.json의 JSON 형식이 올바르지 않습니다.")
    print2()
    print('*** 디버깅 용 ***')
    print(quizzes)
    print2()
    print(state)

    # 
    for quiz in quizzes:
        # q = Quiz(quiz.get("id"))
        q = Quiz(**quiz)
        q.display()
        while True:
            try:
                user_answer = int(input("🤔 답은 몇번일까요? (번호로 입력): "))
                if user_answer < 1 or user_answer > 4:
                    raise ValueError
                break
            except ValueError:
                print("‼️ 올바른 숫자를 입력하세요!\n")
            
        # 정답 여부 판별
        print("◻️" * 30)
        print("◻️◻️◻️◻️◻️", " 👏👏 정답!! 👏👏 " if q.is_correct(user_answer) else " ❌ 틀렸어요... 😭", "◻️◻️◻️◻️◻️")
        print("◻️" * 30)
        print2()

if __name__ == "__main__":
    main()