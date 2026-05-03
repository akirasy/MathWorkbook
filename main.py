import yaml
import random
from fpdf import FPDF

class MathPDF(FPDF):
    def add_worksheet_page(self, title):
        self.add_page()
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(5)

    def draw_problem_expanded(self, x, y, index, top, bot, op):
        # Draw Question Number
        self.set_font("Helvetica", "I", 8)
        self.set_xy(x - 5, y)
        self.cell(10, 5, f"{index}.", ln=False)

        # Draw Math Problem
        self.set_font("Courier", "B", 20)
        self.set_xy(x, y)
        self.cell(25, 10, str(top).rjust(3), ln=False, align="R")
        self.set_xy(x, y + 10)
        self.cell(25, 10, f"{op} {str(bot).rjust(2)}", ln=False, align="R")
        self.line(x + 5, y + 20, x + 30, y + 20)

    def draw_problem_list(self, x, y, index, top, bot, op):
        # Draw Question Number
        self.set_font("Helvetica", "I", 8)
        self.set_xy(x - 5, y + 2)
        self.cell(10, 5, f"{index}.", ln=False)

        # Draw Math Problem
        self.set_font("Courier", "B", 14)
        self.set_xy(x, y)
        display_op = "÷" if op == "/" else op
        self.cell(28, 10, f"{str(top).rjust(3)} {display_op} {str(bot).rjust(3)}", ln=False, align="L")
        self.cell(8, 10, "=", ln=False, align="C")
        self.cell(20, 10, "_______", ln=False, align="L")

    def draw_problem_grid(self, x, y, index, top, bot, op):
        # Draw Question Number
        self.set_font("Helvetica", "I", 8)
        self.set_xy(x + 1, y + 1)
        self.cell(10, 5, f"{index}.", ln=False)

        # Draw Math Problem
        self.rect(x, y, 35, 15)
        self.set_font("Helvetica", "B", 10)
        self.set_xy(x + 6, y + 2)
        display_op = "÷" if op == "/" else op
        self.cell(28, 5, f"{top} {display_op} {bot}", ln=False, align="L")
        self.set_xy(x + 5, y + 8)
        self.set_font("Helvetica", "", 8)
        self.cell(28, 5, "Ans: ________", ln=False, align="L")

    def draw_problem_division(self, x, y, index, dividend, divisor):
        # Question Number
        self.set_font("Helvetica", "I", 8)
        self.set_xy(x - 5, y)
        self.cell(10, 5, f"{index}.", ln=False)
        self.set_font("Courier", "B", 16)

        # Divisor
        divisor_str = str(divisor)
        self.set_xy(x - 2, y + 5)
        self.cell(10, 10, divisor_str.rjust(2), ln=False, align="R")

        # Dividend
        div_str = str(dividend)
        self.set_xy(x + 12, y + 5)
        self.cell(20, 10, div_str, ln=False, align="L")

        # Placeholder Oblique Bracket
        line_w = 5 + (len(div_str) * 4)
        self.line(x + 10, y + 6, x + 10 + line_w, y + 6) # Top Roof
        self.line(x + 10, y + 6, x + 8, y + 14)         # Side Slant

    def add_answer_key(self, all_answers):
        self.add_page()
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Answer Key", ln=True, align="C")
        self.ln(10)

        for section_title, answers in all_answers.items():
            self.set_font("Courier", "B", 12)
            self.cell(0, 10, section_title, ln=True)
            self.set_font("Courier", size=10)

            line_str = ""
            for i, (t, b, o, res) in enumerate(answers, 1):
                display_op = "÷" if o == "/" else o
                ans_text = f"{i}. {t}{display_op}{b}={res}"
                line_str += ans_text.ljust(25)

                if i % 4 == 0:
                    self.cell(0, 8, line_str, ln=True)
                    line_str = ""
            if line_str:
                self.cell(0, 8, line_str, ln=True)
            self.ln(5)

def load_config(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def run_generator():
    config_data = load_config('config.yml')
    pdf = MathPDF()
    all_answers = {}
    
    for tier in config_data['tiers']:
        layout = tier.get('layout', 'expanded')
        op = tier['operation']

        # Determine page capacity and grid spacing
        if op == "/":
            problems_per_page, cols = 16, 4
            y_spacing = 65
            y_base = 27
        elif layout == "grid":
            problems_per_page, cols = 50, 5
            y_spacing = 22
            y_base = 30
        elif layout == "list":
            problems_per_page, cols = 40, 2
            y_spacing = 12
            y_base = 30
        else:
            problems_per_page, cols = 24, 4
            y_spacing = 40
            y_base = 40

        total_problems = tier['pages'] * problems_per_page
        
        for p_idx in range(total_problems):
            local_idx = p_idx % problems_per_page
            
            if local_idx == 0:
                page_num = p_idx // problems_per_page + 1
                current_page_title = f"{tier['name']} - Part {page_num}"
                pdf.add_worksheet_page(current_page_title)
                all_answers[current_page_title] = []

            if op == "/":
                d_digits = tier.get('dividend_digit', 3)
                v_digits = tier.get('divisor_digit', 1)

                q_digits = max(1, d_digits - v_digits + 1)
                divisor = random.randint(10**(v_digits-1), (10**v_digits)-1)
                quotient = random.randint(10**(q_digits-1), (10**q_digits)-1)
                dividend = quotient * divisor

                if len(str(dividend)) > d_digits:
                    dividend = random.randint(10**(d_digits-1), (10**d_digits)-1)
                    quotient = dividend // divisor

                res, top, bot = quotient, dividend, divisor
            else:
                top = random.randint(tier['min_top'], tier['max_top'])
                bot = random.randint(tier['min_bot'], tier['max_bot'])
                if op == "-" and top < bot:
                    top, bot = bot, top
                res = (top + bot) if op == "+" else (top - bot) if op == "-" else (top * bot)

            all_answers[current_page_title].append((top, bot, op, res))
            
            x_base = 15 if layout == "grid" else 20
            x_spacing = 38 if layout == "grid" else 90 if layout == "list" else 45

            x = x_base + (local_idx % cols * x_spacing)
            y = y_base + (local_idx // cols * y_spacing)

            if op == "/" and layout == "expanded":
                pdf.draw_problem_division(x, y, local_idx + 1, top, bot)
            elif layout == "grid":
                pdf.draw_problem_grid(x, y, local_idx + 1, top, bot, op)
            elif layout == "list":
                pdf.draw_problem_list(x, y, local_idx + 1, top, bot, op)
            else:
                pdf.draw_problem_expanded(x, y, local_idx + 1, top, bot, op)
            
    pdf.add_answer_key(all_answers)
    pdf.output(config_data['workbook_name'])
    print(f"Workbook generated: {config_data['workbook_name']}")

if __name__ == "__main__":
    run_generator()

