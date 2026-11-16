from platforms.telegram import bot


try:
    if __name__ == "__main__":
        bot.main()
finally:
    print("Program terminated!")