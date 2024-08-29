Peter Sharpe's PhD thesis @ MIT AeroAstro, Sept. 2024

Title: **Accelerating Practical Engineering Design Optimization with
Computational Graph Transformations**

Abstract:

> Multidisciplinary design optimization has immense potential to improve conceptual design workflows
> for large-scale engineered systems, such as aircraft. However, despite remarkable theoretical progress
> in advanced optimization methods in recent decades, practical industry adoption of such methods
> lags far behind.
> This thesis identifies the root causes of this theory-to-practice gap and addresses
> them by introducing a new paradigm for computational design optimization frameworks called code
> transformations. Code transformations encompass a variety of computational-graph-based scientific
> computing strategies (e.g., automatic differentiation, automatic sparsity detection, problem auto-scaling)
> that automatically analyze, augment, and accelerate the user’s code before passing it to a modern gradient-
> based optimization algorithm.
> 
> This paradigm offers a compelling combination of ease-of-use, computational speed, and modeling
> flexibility, whereas existing paradigms typically make sacrifices in at least one of these key areas. Con-
> sequently, code transformations present a competitive avenue for increasing the adoption of advanced
> optimization techniques in industry, all without placing the burden of deep expertise in applied mathe-
> matics and computer science on end users.
> 
> The major contributions of this thesis are fivefold. First, it introduces the concept of code transfor-
> mations as a possible foundation for an MDO framework and demonstrates their practical feasibility
> through aircraft design case studies. Second, it implements several common aircraft analyses in a form
> compatible with code transformations, providing a practical illustration of the opportunities, challenges,
> and considerations here. Third, it presents a novel technique to automatically trace sparsity through
> certain external black-box functions by exploiting IEEE 754 handling of not-a-number (NaN) values.
> Fourth, it proposes strategies for efficiently incorporating black-box models into a code transformation
> framework through physics-informed machine learning surrogates, demonstrated with an airfoil aero-
> dynamics analysis case study. Finally, it shows how a code transformations paradigm can simplify the
> formulation of other optimization-related aircraft development tasks beyond just design, exemplified by
> aircraft system identification and performance reconstruction from minimal flight data.
> 
> Taken holistically, these contributions aim to improve the accessibility of advanced optimization
techniques for industry engineers, making large-scale conceptual multidisciplinary design optimization
more practical for real-world systems.

[Link to PDF](./sharpe-pds-phd-AeroAstro-2024-thesis.pdf)

[Link to Video of PhD Defense](https://www.youtube.com/watch?v=g8DodWYN3BU)

Citation:
```bibtex
@phdthesis{aerosandbox_phd_thesis,
   title = {Accelerating Practical Engineering Design Optimization with Computational Graph Transformations},
   author = {Sharpe, Peter D.},
   school = {Massachusetts Institute of Technology}, 
   year = {2024},
}
```
