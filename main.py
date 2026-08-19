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


def save_json(file_path, dict):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            dict,
            f,
            ensure_ascii=False,
            indent=2,
        )


"""
반드시 클래스여야 하는가는 아래 기준으로 판단했음.
- 함께 유지해야 할 상태가 있는가?
- 그 상태를 다루는 동작이 여러 개 있는가?

1. 퀴즈 진행: 아래 클래스들을 오케스트레이션 -> QuizGame
2. 퀴즈 생성과 출제: 퀴즈 문제 출력 / 정답과 사용자의 답 비교 -> Quiz
3. 퀴즈 목록 관리: 퀴즈 문항 추가 / 퀴즈 목록 보여주기 -> QuizManager
4. 점수 관리: 퀴즈 풀이 후 점수 반영 / 점수 통보 / 최고 점수 기록 및 갱신 -> ScoreManager
"""


class QuizManager:
    """
    - 퀴즈 문항 추가
    - 퀴즈 목록 보여주기
    """
    def __init__(self, n, level):
        try:
            self.quizzes = load_json(QUIZ_DATA_FILE)
            self.qty_quizzes = len(self.quizzes)
            self.filtered_quizzes = [quiz for quiz in self.quizzes if quiz.get("level") == level][:n]
        except FileNotFoundError:
            print(f"{SYS} 퀴즈 파일을 찾을 수 없어 기본 퀴즈로 대체합니다.")
            self.quizzes = DEFAULT_QUIZ
        except json.JSONDecodeError:
            print(f"{SYS} data.json의 JSON 형식이 올바르지 않습니다.")

    def add(self):
        print(SYS, "문제를 입력해주세요.")
        a = input("question: ")
        # choices
        b = int(input("객관식으로 하려면 숫자 1, 주관식으로 하려면 숫자 2를 입력하세요: ").strip())
        if b == 1:
            print(SYS, "선택지를 4개 입력해주세요.")
            c1 = input("선택 1: ")
            c2 = input("선택 2: ")
            c3 = input("선택 3: ")
            c4 = input("선택 4: ")
            f = int(input("정답은 몇번으로 할까요? :").strip())
            # 퀴즈 난이도 자동 판별
            if (len(c1)+len(c2)+len(c3)+len(c4)) / 4 > 6:
                level = 1
            else:
                level = 0
        else: 
            f = input("정답을 입력해주세요 :")
            # 퀴즈 난이도 자동 판별
            level = 2
        new_quiz = {
            "id": self.qty_quizzes,
            "level": level,
            "question": a,
            "choices": [],
            "answer":f 
        }

        self.quizzes.append(new_quiz)

        save_json(QUIZ_DATA_FILE, self.quizzes)

    def list(self):
        print(SYS, "퀴즈 전체 목록을 출력합니다. ----------------------------")
        for quiz in self.quizzes:
            print()
            print(quiz)
            print()

        print(SYS, "퀴즈 전체 목록 끝 ----------------------------")




class ScoreManager:
    """
    퀴즈 풀이 후 점수 반영 / 점수 통보 / 최고 점수 기록 및 갱신
    """
    def __init__(self):
        self.current_score = 0
        try:    
            self.max_score = load_json(STATE_FILE).get("max_score")
        except FileNotFoundError:
            return f"{SYS} {STATE_FILE} 파일을 찾을 수 없습니다."
        except json.JSONDecodeError:
            return f"{SYS} data.json의 JSON 형식이 올바르지 않습니다."

    def check(self):
        return self.current_score

    def max(self):
        return self.max_score
    
    def record(self):
        self.current_score += 1
        
    def finish(self):
        # 퀴즈 게임이 끝났을 때 총점을 max_score와 비교하여 갱신하거나 유지함.
        if self.current_score > self.max_score:
            self.max_score = self.current_score
            save_json(STATE_FILE, "max_score", self.max_score)
            return f"{SYS} 축하합니다. 최고 점수가 갱신되었습니다! ❤️‍🔥"
        return f"{SYS} 지금까지의 최고 점수는 {self.max_score} 입니다."
    
            
class QuizGame:
    # level: easy(4지선다), normal(4지선다), hard(주관식)
    def __init__(self, n, level, quiz_manager, score_manager):
        self.quiz_manager = quiz_manager
        self.score_manager = score_manager
        self.n = n
        self.level = level

    def start(self):
        self.score_manager.reset()

        # 퀴즈 목록 가져오기
        for quiz in self.quiz_manager.filter(self.n, self.level):
            # 개별 퀴즈 생성
            q = Quiz(**quiz)
            # 퀴즈 출력
            q.display()

            # 답 입력받기
            while True:
                try:
                    user_answer = int(input("🤔 답은 몇번일까요? (번호로 입력): ").strip())
                    if user_answer < 1 or user_answer > 4:
                        raise ValueError
                    break
                except ValueError:
                    print("‼️ 올바른 숫자를 입력하세요!\n")
            
            # 정답 여부 판별
            if q.is_correct(user_answer):
                result = " 👏👏 정답!! 👏👏 "
            else:
                result = " ❌ 틀렸어요... 😭"
        
            # 정답 여부 출력
            print("◻️" * 30)
            print("◻️◻️◻️◻️◻️", result, "◻️◻️◻️◻️◻️")
            print("◻️" * 30)
            print2()

        # 퀴즈 종료
        self.score_manager.finish()  # 점수 매니저가 최고 기록 점수 확인 후 갱신
        print(SYS, "모든 문제를 다 풀었습니다.\n")
        print("◻️" * 40)
        print("◻️", " " * 10, " 퀴즈 결과", " " * 14, "◻️")
        print("◻️", " "  * 10, f" 총 문항수: {self.n}", " " * 11, "◻️")
        print("◻️", " "  * 10, f" 정답 개수: {self.score_manager.check()}", " " * 11, "◻️")
        print("◻️", " "  * 10, f" 최고기록: {self.score_manager.max()}", " " * 10, "◻️")
        print("◻️" * 40)



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
    # 퀴즈 매니저 생성
    quiz_manager = QuizManager()

    # 점수 매니저 생성
    score_manager = ScoreManager()

    # 메뉴 보여주고 시작
    while True:
        while True:
            try:
                print(SYS, "원하는 메뉴를 선택하세요.")
                menu = int(input("퀴즈 풀기(1) / 퀴즈 추가(2) / 퀴즈 목록 보기(3) / 최고점수 확인(4) ").strip())
                break
            except:
                print(SYS, "정확한 숫자를 입력해주세요.")

        # 퀴즈 풀기(1)        
        if menu == 1:
            while True:
                try:
                    n = int(input(SYS, "문제를 몇개 풀고 싶은가요? :").strip())
                    break
                except:
                    print(SYS, "정확하게 숫자로 입력해주세요")

            while True:
                try:
                    level = int(input(SYS, "난이도를 선택해주세요. 1(쉬움)/2(중간)/3(어려움)").strip())
                    break
                except:
                    print(SYS, "정확하게 숫자로 입력해주세요")

            # 퀴즈 진행자 생성
            quiz_game = QuizGame(n, level, quiz_manager, score_manager)

        # 퀴즈 추가(2)
        elif menu == 2:
            quiz_manager.add()

        # 퀴즈 목록 보기(3)
        elif menu == 3:
            quiz_manager.list()

        # 최고점수 확인(4)
        else:
            print(SYS, f"최고 점수: {score_manager.max()}")


if __name__ == "__main__":
    main()