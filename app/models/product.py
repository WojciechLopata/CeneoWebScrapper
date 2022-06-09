
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
class Product():
    def __init__(self,product_id):
            self.img = mpimg.imread(f'/plots/{product_id}.png')
    def display(self):
        imgplot = plt.imshow(self.img)
        plt.show()

            
            