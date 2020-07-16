#include <iostream>
#include <cmath>
#include <fstream>
#include <cstdio>
void initializationMaterial();
void materialSelection();

double YoungModulus_Density[2];
double K_i[2][2] = {
                    {1.0, -1.0},
                    {-1.0, 1.0}
};
double F_i[2][1] = {
                    {0.5},
                    {0.5}
};

class Material
{
  public:
    unsigned long long YoungModulus;
    unsigned short density;

    void GPa(unsigned short YM)
    {
      YoungModulus = YM * pow(10, 9);
    }
};

void solution(int N, double *nodes, double *U)
{
  std::ofstream file("finiteElementMethod.txt");
  file << "#x y" << '\n';
  file << 0 << ' ' << 0 <<'\n';
  for (int i = 0; i < N; i++)
    file << nodes[i] << ' ' << U[i] <<'\n';
  file.close();
  FILE *gp = popen("gnuplot -persist","w");
  fprintf(gp, "plot 'finiteElementMethod.txt' using 1:2 with lines\n");
}

void solveMatrix (int N, double *K_UP_DOWN_diagonal, double *Kdiagonal, double *F, double *U)
{
	double m;
	for (int i = 1; i < N; i++)
	{
		m = K_UP_DOWN_diagonal[i]/Kdiagonal[i-1];
		Kdiagonal[i] = Kdiagonal[i] - m*K_UP_DOWN_diagonal[i-1];
		F[i] = F[i] - m*F[i-1];
	}

	U[N-1] = F[N-1]/Kdiagonal[N-1];

	for (int i = N - 2; i >= 0; i--)
    {
		U[i]=(F[i]-K_UP_DOWN_diagonal[i]*U[i+1])/Kdiagonal[i];
    }
}

double* createF(int N)
{
  double *F = new double[N];
  double c = YoungModulus_Density[1] / (N * N * YoungModulus_Density[0]);
  for (int i = 0; i < N-1; i++) {
    F[i] = c;
  }
  F[N-1] = 0.5 * c;
  return F;
}

double* createKdiagonal(int N)
{
  double *Kdiagonal = new double[N];
  for (int i = 0; i < N-1; i++) {
    Kdiagonal[i] = 2.0;
  }
  Kdiagonal[N-1] = 1.0;
  return Kdiagonal;
}

double* createK_UP_DOWN_diagonal(int N)
{
  double *K_UP_DOWN_diagonal = new double[N];
  for (int i = 0; i < N; i++) {
    K_UP_DOWN_diagonal[i] = -1.0;
  }
  return K_UP_DOWN_diagonal;
}


double* createU(int N)
{
  double *U = new double[N];
  for (int i = 0; i < N-1; i++) {
    U[i] = 0.0;
  }
  return U;
}

double** transp(double** a,int n, int m)
{
  int i,j;
  double **b;
  b=new double *[n+1];
  for (i=0;i< n+1;i++){
    b[i]=new double[m];
     }
   for (i=0;i< n+1;i++)
     for (j=0;j< m;j++)
       b[i][j]=a[j][i];
 return b;
}

double* createNodes(int N)
{
  double *nodes = new double[N+1];
  for (int i = 1; i < N+1; i++) {
    nodes[i] = (1.0 * i ) / N;
  }
  return nodes;
}

int number_elements()
{
  int N;
  std::cout << "Enter the number of elements: ";
  std::cin >> N;
  std::cout << '\n';
  return N;
}

short textMaterialSelection()
{
  short choice;
  std::cout << '\n' << '\n';
  std::cout << "******************Choose material****************** " << '\n';
  std::cout << '\n';
  std::cout << "1.Plumbum                                2.Aluminum " << '\n';
  std::cout << "3.Silver                                 4.Cuprum   " << '\n';
  std::cout << "5.Steel                                  6.Own data " << '\n';
  std::cout << '\n' << "Enter number: ";
  std::cin >> choice;
  std::cout << '\n';
  return choice;
}
