import random

class MathQuestionGenerator:
    def _validate_range(self, min_val, max_val):
        """Ensures min_val <= max_val by swapping them if necessary."""
        if min_val > max_val:
            return max_val, min_val
        return min_val, max_val

    def _get_digit_range(self, digits):
        """Converts digit count into min and max bounds."""
        if digits <= 1:
            return 1, 9
        min_val = 10 ** (digits - 1)
        max_val = (10 ** digits) - 1
        return min_val, max_val

    def addition(self, min_top, max_top, min_bot, max_bot, count=4):
        min_top, max_top = self._validate_range(min_top, max_top)
        min_bot, max_bot = self._validate_range(min_bot, max_bot)

        questions = []
        for _ in range(count):
            top = random.randint(min_top, max_top)
            bottom = random.randint(min_bot, max_bot)
            questions.append({
                "top": top,
                "operator": "+",
                "bottom": bottom,
                "answer": top + bottom
                })
        return questions

    def subtraction(self, min_top, max_top, min_bot, max_bot, count=4):
        min_top, max_top = self._validate_range(min_top, max_top)
        min_bot, max_bot = self._validate_range(min_bot, max_bot)

        questions = []
        for _ in range(count):
            top = random.randint(min_top, max_top)
            bottom = random.randint(min_bot, max_bot)
            questions.append({
                "top": top,
                "operator": "-",
                "bottom": bottom,
                "answer": top - bottom
                })
        return questions

    def multiplication(self, min_top, max_top, digit_bot, count=4):
        min_top, max_top = self._validate_range(min_top, max_top)
        min_bot, max_bot = self._get_digit_range(digit_bot)

        questions = []
        for _ in range(count):
            top = random.randint(min_top, max_top)
            bottom = random.randint(min_bot, max_bot)
            questions.append({
                "top": top,
                "operator": "×",
                "bottom": bottom,
                "answer": top * bottom
                })
        return questions

    def division(self, min_top, max_top, digit_bot, count=4):
        min_top, max_top = self._validate_range(min_top, max_top)
        min_bot, max_bot = self._get_digit_range(digit_bot)

        questions = []
        for _ in range(count):
            bottom = random.randint(min_bot, max_bot)

            min_ans = (min_top + bottom - 1) // bottom
            max_ans = max_top // bottom

            ans = random.randint(min_ans, max_ans)
            top = bottom * ans

            questions.append({
                "top": top,
                "operator": "÷",
                "bottom": bottom,
                "answer": ans
                })
        return questions
