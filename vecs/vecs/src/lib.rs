use std::{fmt::Debug, path::Iter, vec};

/// The basis of a vector space is a set of linearly independent 
/// vectors that span that space


#[derive(PartialEq, Debug, Copy, Clone)]
struct Vector<const N: usize>([f32; N]);


impl <const N: usize> Vector<N> {

    pub fn new<T: Into<f32> + Copy>(components: [T; N]) -> Self {
        Vector(components.map(|x| x.into()))
    }

    /// Computes the length of the Vector
    pub fn length(&self) -> f32 {
        let length: f32 = self.0.iter().map(|x| {
            x * x
        }).sum();
        
        length.sqrt()
    }

    /// Adds to vectors and returns a new one
    pub fn static_add(v1: Self, v2: &Self) -> Self {
        assert!(v1.0.len() == v2.0.len());
        
        let mut result = [f32::default(); N];
        for x in 0..v1.0.len() {
            result[x] = v1.0[x] + v2.0[x];
        }
        
        Vector(result)
    }

    /// Scales the provided vector and returns a new one
    pub fn static_scale(v1: Self, scalar: f32) -> Self {
        let mut result = [f32::default(); N];
        for x in 0..N {
            result[x] = v1.0[x] * scalar;
        }
        Vector::new(result)
    }

    /// Addition on the instance
    pub fn add(&mut self, other: &Self) {
        assert!(self.0.len() == other.0.len());
        for x in 0..self.0.len() {
            self.0[x] = self.0[x] + other.0[x];
        }
    }

    /// Addition on the instance
    pub fn scale(&mut self, scalar: f32) {
        for x in 0..self.0.len() {
            self.0[x] = self.0[x] * scalar;
        }
    }

    /// Apply a lnear transformation to vector, returning a new vector
    pub fn static_transform(v1: Self, matrix: &Matrix<N, N>) -> Self {
    
        let mut result = [0.0; N];
        for i in 0..matrix.0.len() {
            let row = &matrix.0[i];
            let mut sum = 0.0;
            for j in 0..N {
                sum += row.0[j] * v1.0[j];
            }
            result[i] = sum;
        }
        Vector::new(result)
    }

    pub fn transform(&mut self, matrix: &Matrix<N, N>) {   
        let mut result = [0.0; N];             
        for i in 0..matrix.0.len() {
            let row = &matrix.0[i];
            let mut sum = 0.0;
            for j in 0..N {
                sum += row.0[j] * self.0[j];
            }
            result[i] = sum;
        }   

        for i in 0..N {
            self.0[i] = result[i];
        }     
    }

}


/// A Matrix representation as a collection of M Vectors of N elements each
#[derive(Copy, Clone, Debug)]
struct Matrix<const M: usize, const N: usize>([Vector<N>; M]);


impl <const M: usize, const N: usize> Matrix<M, N> {

    pub fn new(rows: [Vector<N>; M]) -> Self {
        Matrix(rows)
    }
}

const COUNTER_CLOCKWISE_90_DEGREES_TRANSFORMATION: Matrix<2, 2> = Matrix([
    Vector([0.0, 1.0]),
    Vector([-1.0, 0.0])
]);
    

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let v1 = Vector::new([1.0, 2.0]);
        let mut v2 = Vector::new([3.0, -1.0]);

        assert_eq!(Vector::new([4.0, 1.0]), Vector::static_add(v1.clone(), &v2));        
        v2.add(&v1);       
        assert_eq!(Vector::new([4.0, 1.0]), v2);

        let transformation1 = Matrix::new([
            Vector::new([2.0, 1.0]),
            Vector::new([3.0, -2.0]),
        ]);
        assert_eq!(
            Vector::static_transform(Vector::new([5.0, 7.0]), &transformation1),
            Vector::new([17.0, 1.0])
        );

        let mut v3 = Vector::new([5.0, 7.0]);        
        v3.transform(&transformation1);
        assert_eq!(
            v3,
            Vector::new([17.0, 1.0])
        );
    }
}
