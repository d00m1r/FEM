#include "finiteElementMethod.h"

Material plumbum;
Material aluminum;
Material silver;
Material cuprum;
Material steel;

int main()
{
  initializationMaterial();
  materialSelection();
  int N = number_elements();
  double *nodes = createNodes(N);
  double *F = createF(N);
  double *U = createU(N);
  double *Kdiagonal = createKdiagonal(N);
  double *K_UP_DOWN_diagonal = createK_UP_DOWN_diagonal(N);
  solveMatrix (N, K_UP_DOWN_diagonal, Kdiagonal, F, U);
  solution(N, nodes, U);

  delete [] nodes;
  delete [] F;
  delete [] U;
  delete [] Kdiagonal;
  delete [] K_UP_DOWN_diagonal;

  return 0;
}

void initializationMaterial()
{
  plumbum.GPa(18);
  plumbum.density = 11340;

  aluminum.GPa(70);
  aluminum.density = 2712;

  silver.GPa(80);
  silver.density = 10500;

  cuprum.GPa(110);
  cuprum.density = 8900;

  steel.GPa(200);
  steel.density = 7856;
}

void materialSelection()
{
tryAgain:
  short choice = textMaterialSelection();
  switch (choice) {
    case 1:
      YoungModulus_Density[0] = plumbum.YoungModulus;
      YoungModulus_Density[1] = plumbum.density;
      break;
    case 2:
      YoungModulus_Density[0] = aluminum.YoungModulus;
      YoungModulus_Density[1] = aluminum.density;
      break;
    case 3:
      YoungModulus_Density[0] = silver.YoungModulus;
      YoungModulus_Density[1] = silver.density;
      break;
    case 4:
      YoungModulus_Density[0] = cuprum.YoungModulus;
      YoungModulus_Density[1] = cuprum.density;
      break;
    case 5:
      YoungModulus_Density[0] = steel.YoungModulus;
      YoungModulus_Density[1] = steel.density;
      break;
    case 6:
      std::cout << "Enter Young Modulus: ";
      std::cin >> YoungModulus_Density[0];
      std::cout << '\n' << "Enter density: ";
      std::cin >> YoungModulus_Density[1];
      break;
    default:
      std::cout << "ERROR, select again " << '\n';
      goto tryAgain;
  }
}
