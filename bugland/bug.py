
import numpy

class Bug(object):
    """
    A Bug is a sort of sprite.

    Creates a Bug with the specified name and whose pixel
    representation is given by ``patch`` (a 2D array where 0 is the
    background and 1 is a pixel of the bug). The ``mask`` of the Bug
    is the space that "belongs" to it (so two bugs are said to overlap
    if their masks overlap). The mask defaults to the same thing as
    the patch if it is not given.
    """

    def __init__(self, name, patch, mask = None):
        self.name = name
        self.patch = numpy.array(patch)
        if mask is None:
            self.mask = self.patch
        else:
            self.mask = numpy.array(mask)

    def rotate(self, angle):
        """
        Rotate the Bug by the specified angle, in degrees. Only
        orthogonal rotations (multiples of 90 degrees) are supported,
        so one may choose between 0, 90, 180 and 270.
        """
        angle %= 360
        if angle not in (0, 90, 180, 270):
            raise ValueError('angle must be one of: 0, 90, 180, 270')
        if angle == 0:
            return self
        if angle == 90:
            return Bug(self.name,
                       self.patch.T,
                       self.mask.T).hflip()
        if angle >= 180:
            return self.hflip().vflip().rotate(angle-180)

    def hflip(self):
        """
        Returns a Bug that's flipped horizontally relative to this one
        (symmetry around the y axis).
        """
        return Bug(self.name,
                   self.patch[:, ::-1],
                   self.mask[:, ::-1])

    def vflip(self):
        """
        Returns a Bug that's flipped vertically relative to this one
        (symmetry around the x axis).
        """
        return Bug(self.name,
                   self.patch[::-1],
                   self.mask[::-1])

    def scale(self, xscale, yscale = None):
        """
        Returns a new Bug scaled as specified. xscale and yscale must
        be integers. Each pixel of the original bug will be mapped to
        a xscale by yscale block of pixels.
        """
        if yscale is None: yscale = xscale
        if not isinstance(xscale, int) or not isinstance(yscale, int):
            raise TypeError("xscale and yscale must be integers.")
        prows, pcols = self.patch.shape
        mrows, mcols = self.mask.shape
        patch = numpy.zeros((prows*yscale, pcols*xscale))
        mask = numpy.zeros((mrows*yscale, mcols*xscale))
        for i in xrange(yscale):
            for j in xrange(xscale):
                patch[i:prows*yscale:yscale, j:pcols*xscale:xscale] = self.patch
                mask[i:mrows*yscale:yscale, j:mcols*xscale:xscale] = self.mask
        return Bug(self.name, patch, mask)

    def margin(self, margin):
        """
        Creates a Bug whose mask is the patch enlarged by margin
        pixels all around.
        """
        mr, mc = self.patch.shape[0]+margin*2, self.patch.shape[1]+margin*2
        mask = numpy.zeros((mr, mc), dtype = 'int')
        m = margin*2 + 1
        for i in xrange(m):
            for j in xrange(m):
                mask[i:mr-m+1+i, j:mc-m+1+j] |= self.patch
        b = Bug(self.name,
                self.patch,
                mask)
        return b

    def total_mask(self):
        """
        Creates a Bug whose mask is the whole rectangle.
        """
        return Bug(self.name,
                   self.patch,
                   numpy.ones(self.mask.shape))

    def fit_mask(self):
        """
        Returns a Bug whose mask is this Bug's patch.
        """
        return Bug(self.name,
                   self.patch,
                   self.patch)

    def __str__(self):
        return self.name + '\n' + '\n'.join(' '.join('x' if x else ' ' for x in row) for row in self.patch)

    h = property(lambda self: self.patch.shape[0], doc = "Property that returns the bug's height.")
    w = property(lambda self: self.patch.shape[1], doc = "Property that returns the bug's width.")

    mh = property(lambda self: self.mask.shape[0], doc = "Property that returns the bug's mask's height.")
    mw = property(lambda self: self.mask.shape[1], doc = "Property that returns the bug's mask's height.")

    marginh = property(lambda self: (self.mh-self.h)/2, doc = "Property that returns the difference between the bug's height and the bug's mask's height.")
    marginw = property(lambda self: (self.mw-self.w)/2, doc = "Property that returns the difference between the bug's width and the bug's mask's width.")
