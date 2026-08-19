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


def input_int(prompt, minimum=None, maximum=None):
    """
    정수를 정상적으로 입력할 때까지 반복해서 입력받습니다.
    """

    while True:
        try:
            value = int(input(prompt).strip())

            if minimum is not None and value < minimum:
                raise ValueError

            if maximum is not None and value > maximum:
                raise ValueError

            return value

        except ValueError:
            print(f"{SYS} 올바른 숫자를 입력해주세요.")
            

class QuizManager:
    """
    퀴즈 목록을 불러오고 관리합니다.

    - 퀴즈 필터링
    - 퀴즈 문항 추가
    - 퀴즈 목록 출력
    """

    def __init__(self):
        try:
            data = load_json(QUIZ_DATA_FILE)

            if not isinstance(data, list):
                raise ValueError(
                    "quiz.json의 최상위 데이터는 배열이어야 합니다."
                )

            self.quizzes = data

        except FileNotFoundError:
            print(
                f"{SYS} 퀴즈 파일을 찾을 수 없어 "
                "기본 퀴즈로 대체합니다."
            )

            # DEFAULT_QUIZ에는 level이 없으므로 기본값 1을 추가합니다.
            self.quizzes = [
                {
                    **quiz,
                    "level": quiz.get("level", 1),
                }
                for quiz in DEFAULT_QUIZ
            ]

        except (json.JSONDecodeError, ValueError) as error:
            print(f"{SYS} quiz.json을 읽을 수 없습니다: {error}")

            self.quizzes = [
                {
                    **quiz,
                    "level": quiz.get("level", 1),
                }
                for quiz in DEFAULT_QUIZ
            ]

    def filter(self, n, level):
        """
        원하는 난이도의 문제를 최대 n개 반환합니다.
        """

        filtered_quizzes = [
            quiz
            for quiz in self.quizzes
            if quiz.get("level") == level
        ]

        return filtered_quizzes[:n]

    def add(self):
        print(SYS, "문제를 입력해주세요.")

        question = input("question: ").strip()

        quiz_type = input_int(
            "객관식은 1, 주관식은 2를 입력하세요: ",
            minimum=1,
            maximum=2,
        )

        if quiz_type == 1:
            print(SYS, "선택지를 4개 입력해주세요.")

            choices = [
                input(f"선택 {number}: ").strip()
                for number in range(1, 5)
            ]

            answer = input_int(
                "정답은 몇 번인가요? ",
                minimum=1,
                maximum=4,
            )

            # 기존 조건 유지:
            # 선택지의 평균 글자 수가 6을 넘으면 level 1
            average_length = sum(
                len(choice) for choice in choices
            ) / len(choices)

            if average_length > 15:
                level = 1
            else:
                level = 0

        else:
            choices = []
            answer = input("정답을 입력해주세요: ").strip()
            level = 2

        # 문제 개수가 아니라 가장 큰 ID를 기준으로 다음 ID를 생성합니다.
        next_id = max(
            (
                quiz.get("id", 0)
                for quiz in self.quizzes
            ),
            default=0,
        ) + 1

        new_quiz = {
            "id": next_id,
            "level": level,
            "question": question,
            "choices": choices,
            "answer": answer,
        }

        self.quizzes.append(new_quiz)

        save_json(
            QUIZ_DATA_FILE,
            self.quizzes,
        )

        print(f"{SYS} {next_id}번 문제가 추가되었습니다.")

    def list(self):
        print(
            SYS,
            "퀴즈 전체 목록을 출력합니다."
        )

        for quiz in self.quizzes:
            print()
            print(quiz)

        print()
        print(SYS, "퀴즈 전체 목록 끝")


class ScoreManager:
    """
    퀴즈 풀이 후 점수 반영 / 점수 통보 / 최고 점수 기록 및 갱신
    """
    def __init__(self):
        self.current_score = 0

        try:    
            self.max_score = load_json(STATE_FILE).get("max_score", 0)
        except FileNotFoundError:
            print(f"{SYS} {STATE_FILE} 파일을 찾을 수 없어 새롭게 초기화 합니다.")
            save_json(STATE_FILE, {"max_score": 0})
            print(f"{SYS} state.json 파일을 생성하고 최고점수를 0점으로 초기화했습니다.")
        except json.JSONDecodeError:
            print(f"{SYS} data.json의 JSON 형식이 올바르지 않습니다.")

    def reset(self):
        self.current_score = 0

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
            save_json(STATE_FILE, {"max_score": self.max_score})
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
            if q.is_multiple_choice:
                user_answer = input_int("🤔 답은 몇번일까요? (번호로 입력): ", minimum=1, maximum=len(q.choices))
            else:
                user_answer = input("🤔 정답을 입력하세요: ").strip()
                
            # 정답 여부 판별
            if q.is_correct(user_answer):
                self.score_manager.record()
                result = " 👏👏 정답!! 👏👏 "
            else:
                result = " ❌ 틀렸어요... 😭"
        
            # 정답 여부 출력
            print()
            print("◻️" * 30)
            print("◻️◻️◻️◻️◻️", result, "◻️◻️◻️◻️◻️")
            print("◻️" * 30, "\n")
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
    def __init__(self, id, level, question, choices, answer):
        self.quiz_id = id
        self.level = level
        self.question = question
        self.choices = choices
        self.answer = answer

    @property
    def is_multiple_choice(self):
        """
        choices가 있으면 객관식, 비어 있으면 주관식입니다.
        """

        return bool(self.choices)
    
    def display(self):
        print(f"{self.quiz_id}. {self.question}\n")

        for num, choice in enumerate(self.choices, 1):
            print(f"   ({num}) {choice}")
        print()

    def is_correct(self, user_answer):
        if self.is_multiple_choice:
            return self.answer == user_answer

        # 주관식은 대소문자와 띄어쓰기를 무시합니다.
        correct_answer = "".join(str(self.answer).split()).casefold()

        submitted_answer = "".join(str(user_answer).split()).casefold()

        return correct_answer == submitted_answer



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
        print(SYS, "원하는 메뉴를 선택하세요.")
        menu = input_int(("프로그램 종료(0) / 퀴즈 풀기(1) / 퀴즈 추가(2) / 퀴즈 목록 보기(3) / 최고점수 확인(4) "), minimum=0, maximum=4)

        if menu == 0:
            print(SYS, "프로그램을 종료합니다.")
            quit()

        # 퀴즈 풀기(1)        
        if menu == 1:
            n = input_int(f"{SYS} 몇개의 문제를 풀어볼까요? :", minimum=1)

            selected_difficulty = input_int(
                (
                    f"{SYS} 난이도를 선택해주세요. "
                    "1(쉬움) / "
                    "2(중간) / "
                    "3(어려움): "
                ),
                minimum=1,
                maximum=3,
            )

            # 사용자 입력 1, 2, 3 ->  JSON의 level 0, 1, 2로 변환
            level = selected_difficulty - 1

            # 퀴즈 진행자 생성
            quiz_game = QuizGame(n, level, quiz_manager, score_manager)
            # 퀴즈 진행 시작
            quiz_game.start()

        # 퀴즈 추가(2)
        elif menu == 2:
            quiz_manager.add()

        # 퀴즈 목록 보기(3)
        elif menu == 3:
            quiz_manager.list()

        # 최고점수 확인(4)
        elif menu == 4:
            print(SYS, f"최고 점수: {score_manager.max()}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print2()
        print(SYS, "Ctrl + C가 입력되어 프로그램을 종료합니다.")
        