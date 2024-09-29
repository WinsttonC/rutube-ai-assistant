from utils import get_answer
import os
os.environ["TOKENIZERS_PARALLELISM"] = "true"

def main():
    # user_input = input("Введите ваш запрос: ")
    user_input = "монетизация"
    answer = get_answer(user_input)
    print(answer)

if __name__ == "__main__":
    main()
