import concurrent.futures



"""
def do_something(secs):
    if secs ==1:
        win1 = Tk()
        a = plot_four(win1)
        win1.mainloop()
    if secs ==2:
        win2 = Tk()
        b = plot_four(win2)
        win2.mainloop()
    if secs ==3:
        win2 = Tk()
        c = plot_four(win2)
        win2.mainloop()

    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return f'Done Sleeping...{seconds}'

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        secs = [1,2,3]
        results = executor.map(do_something, secs)"""
