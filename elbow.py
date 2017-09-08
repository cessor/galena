    from numpy import cross, subtract
    from numpy.linalg import norm

    def distance(p, a, b):
        return norm(cross(subtract(b, a), subtract(a, p)))  / norm (subtract(b, a))