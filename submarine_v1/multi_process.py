import concurrent.futures

class multiprocess:
    def __init__(self,parent):
        self.parent = parent

    def start(self, var):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            if var % 50 == 0:
                executor.submit(self.parent.plot_4.update_graph)
                executor.submit(self.parent.plot_6.output_var)
                executor.submit(self.parent.plot_5.update_sub)
            elif var % 10 == 0:
                executor.submit(self.parent.plot_2.update)
                executor.submit(self.parent.plot_3.rotate_boussole)
