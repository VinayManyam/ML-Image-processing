from detecto import core, utils, visualize

def check(image1):
	 image = utils.read_image(image1)
	 model = core.Model()
	 labels, boxes, scores = model.predict_top(image)
	 visualize.show_labeled_image(image, boxes, labels)
