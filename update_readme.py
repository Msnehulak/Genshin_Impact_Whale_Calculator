import whale_calculator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests

class UpdateDocs:
    def __init__(self):
        self.get_exchange_rate()
        self.get_data()

    def get_data(self):
        WC = whale_calculator.WhaleCalculator()
        data = WC.get_data()

        self.data = {
                "names": [],
                "spend": [],
                "tables": [],
                "colors": [],
                }

        for i in data:
            self.data["names"].append(i["name"])
            self.data["spend"].append(i["spend"])
            self.data["tables"].append(i["table"])
            self.data["colors"].append(i["color"])

    def get_exchange_rate(self):
        try:
            response = requests.get("https://api.frankfurter.app/latest?from=USD&to=EUR", timeout=10)
            if response.status_code == 200:
                self.euro_rate = response.json()["rates"]["EUR"]
        except:
            pass
        self.euro_rate = 0.97
   
    def generate_pie_chart(self):
        categories = self.data["names"]
        values = self.data["spend"]
        colors = self.data["colors"]

        total = sum(values)
        legend_labels = [f'{l}: {v/total*100:1.1f}%' for l, v in zip(categories, values)] 

        fig, ax = plt.subplots(figsize=(14, 8), facecolor='none')

        wedges, _ = ax.pie(
            values, 
            colors=colors, 
            startangle=140, 
            pctdistance=0.95,
            labeldistance=1.1
        )

        ax.legend(
            wedges, 
            legend_labels,
            title="Categories",
            title_fontsize=21,
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            
            fontsize=19,
            frameon=False,
        )

        ax.set_title('Genshin Impact Whale Spend Distribution', pad=15, size=24)

        plt.savefig('spend_chart.png', bbox_inches='tight', transparent=False, facecolor="white")
        plt.close()

    def generate_read_me(self):
        self.generate_table()
        self.generate_pie_chart()

        mark_down = f"""# Genshin Impact - Whale Calculator
This is a calculator that estimates how much a Genshin Impact whale can spend in the game.

To remove randomness and make the result deterministic, the calculator assumes worst-case luck:
- 180 pulls per 5★ character (guaranteed after losing the 50/50)
- 80 pulls per 5★ weapon

**Note:** 
For characters, losing the 50/50 is required to reach the deterministic cost.
For weapons, the model assumes a guaranteed limited 5★ weapon within the pity cycle and does not simulate additional losses.

**!!!** 
The result represents a theoretical maximum and deterministic cost, not an average or realistic outcome.

## Pie Spend Distribution

![Whale Chart](spend_chart.png)

## Table Spend Distribution

{self.table}
"""
        self.write_readme(mark_down)

    def generate_table(self):
        ret = []
        ret.append('| Type | Spend (EUR) | Spend (USD) | Share |')
        ret.append('| :--- | :--- | :--- | :--- |')
        for i in range(0, len(self.data)):
            ret.append(f'|{self.data["tables"][i]}|{self.data["spend"][i] * self.euro_rate}|{float(self.data["spend"][i])} | in progress |'
        ret.append('| |')
        ret.append(f'| **Total** | **{sum(self.data["spend"]) * self.euro_rate} EUR** |{sum(self.data["spend"])}** USD** | **100%** |')

        self.table = ""
        for r in ret:
            self.table += f"{r}\n"

    @staticmethod
    def write_readme(markdown):
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(markdown)

if __name__ == "__main__":
    app = UpdateDocs()
    app.generate_read_me()
