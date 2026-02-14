import yaml
import random
from fpdf import FPDF

class MathPDF(FPDF):
    def add_worksheet_page(self, title):
        self.add_page()
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(5)

    def draw_problem(self, x, y, index, top, bot, op):
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

    def add_answer_key(self, all_answers):
        self.add_page()
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Answer Key", ln=True, align="C")
        self.ln(10)

        # Iterate through each specific Page/Part
        for section_title, answers in all_answers.items():
            self.set_font("Courier", "B", 12)
            self.cell(0, 10, section_title, ln=True)
            self.set_font("Courier", size=10)

            line_str = ""
            # enumerate(answers, 1) ensures numbering always starts at 1 for each Part
            for i, (t, b, o, res) in enumerate(answers, 1):
                ans_text = f"{i}. {t}{o}{b}={res}"
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
    
    problems_per_page = 24
    
    for tier in config_data['tiers']:
        total_problems = tier['pages'] * problems_per_page
        
        for p_idx in range(total_problems):
            local_idx = p_idx % problems_per_page # 0 to 23
            
            # Start a new page and a new answer list for this Part
            if local_idx == 0:
                page_num = p_idx // problems_per_page + 1
                current_page_title = f"{tier['name']} - Part {page_num}"
                pdf.add_worksheet_page(current_page_title)
                all_answers[current_page_title] = [] # Initialize answer list for this specific part
            
            # Logic
            top = random.randint(tier['min_top'], tier['max_top'])
            bot = random.randint(tier['min_bot'], tier['max_bot'])
            op = tier['operation']
            
            if op == "-" and top < bot:
                top, bot = bot, top
            
            if op == "+": res = top + bot
            elif op == "-": res = top - bot
            else: res = top * bot
            
            # Add to the specific Part's list
            all_answers[current_page_title].append((top, bot, op, res))
            
            # Draw on PDF
            pdf.draw_problem(
                20 + (local_idx % 4 * 45), 
                40 + (local_idx // 4 * 40), 
                local_idx + 1, top, bot, op
            )
            
    pdf.add_answer_key(all_answers)
    
    pdf.output(config_data['workbook_name'])
    print(f"Workbook generated: {config_data['workbook_name']}")

if __name__ == "__main__":
    run_generator()

