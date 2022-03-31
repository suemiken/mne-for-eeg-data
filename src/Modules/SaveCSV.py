import os
import csv

def SaveCSV(stock):
    with open("stock.csv", "w", encoding="Shift_jis") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(stock)

    return 0
