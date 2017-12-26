#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct tTempo {
    int hr;
    int min;
    int seg;
} tTempo;

typedef struct tSenha {
    char nome[51];
    char orgao_desejado[51];
    int idade;
    struct tTempo tempo;
} tSenha;

typedef struct tAtendente {
    char cliente[51];
} tAtendente;

typedef struct tOrgao {
    char id[51];
    struct tAtendente* vAtendente;
    int nAtendentes;
    struct tSenha* vSenha;
    int nSenhas;
    int capSenhas;
} tOrgao;

//Leitura do arquivo
void lerOrgao(FILE* input, struct tOrgao* vOrgao);
void lerSenha(FILE* input, tSenha* temp);
void inserirSenha(tSenha* senha, tOrgao* vOrgao, int nOrgaos);
void verificarEspaco(tOrgao* O);

//Implementação das filas de prioridade
int esquerdo (int i);
int direito (int i);
int pai (int i);
void troca (tSenha* V, int P, int i);
int idoso(tSenha senha);
int menorTempo_de_Chegada(tSenha* V, int A, int B);
void heapify (tSenha* V, int T, int i);
void construirPrioridade (tSenha* V, int nSenhas);

//Implementação do atendimento
void executarAtendimento(tOrgao* O, int* nSenhas);
void removerSenha(tSenha* V, int* nSenhas, int* totSenhas);
void imprimirAtendentes(FILE* output, char* ID, tAtendente* V, int nAtendentes);

enum { capInicial = 1000 };

int main (int argc, char* argv[])
{
    //----------------//
    // ABRIR ARQUIVOS
    //----------------//
    
    FILE* input = fopen(argv[1], "r");
    FILE* output = fopen(argv[2], "w");
    
    if (input == NULL)
    {
        printf("Erro ao abrir arquivo!\n");
        exit(1);
    }
    
    //----------------------------------------//
    // CRIAR ESTRUTURA DE ÓRGÃOS & LER ÓRGÃOS
    //----------------------------------------//
    
    int nOrgaos;
    fscanf(input, "%u%*c", &nOrgaos);
    tOrgao* vOrgao = (tOrgao*)malloc(sizeof(tOrgao) * nOrgaos);
    for (int i = 0; i < nOrgaos; i++)
        lerOrgao(input, &vOrgao[i]);
    
    //----------------------//
    // LER E INSERIR SENHAS
    //----------------------//
    
    int nSenhas;
    fscanf(input, "%u%*c", &nSenhas);
    tSenha* temp = (tSenha*)malloc(sizeof(tSenha));
    for (int i = 0; i < nSenhas; i++)
    {
        lerSenha(input, temp);
        inserirSenha(temp, vOrgao, nOrgaos);
    }
    
    for (int i = 0; i < nOrgaos; i++)
        construirPrioridade(vOrgao[i].vSenha, vOrgao[i].nSenhas);
    
    //---------------------//
    // INICIAR ATENDIMENTO
    //---------------------//
    
    while (nSenhas != 0)
    {
        for (int i = 0; i < nOrgaos; i++)
        {
            executarAtendimento(&vOrgao[i], &nSenhas);
            imprimirAtendentes(output, vOrgao[i].id, vOrgao[i].vAtendente, vOrgao[i].nAtendentes);
        }
    }
    
    fclose(input);
    fclose(output);
    return 0;
}

int esquerdo (int i) {
    return (2*i) + 1;
}

int direito (int i) {
    return (2*i) + 2;
}

int pai (int i) {
    return (i-1)/2;
}

void troca (tSenha* V, int P, int i)
{
    tSenha temp = V[i];
    V[i] = V[P];
    V[P] = temp;
}

int idoso(tSenha senha)
{
    if (senha.idade >= 60)
        return 1;
    else
        return 0;
}

int menorTempo_de_Chegada(tSenha* V, int A, int B)
{
    if (V[A].tempo.hr < V[B].tempo.hr)
        return A;
    else if (V[B].tempo.hr < V[A].tempo.hr)
        return B;
    else
    {
        if (V[A].tempo.min < V[B].tempo.min)
            return A;
        else if (V[B].tempo.min < V[A].tempo.min)
            return B;
        else
        {
            if (V[A].tempo.seg < V[B].tempo.seg)
                return A;
            else if (V[B].tempo.seg < V[A].tempo.seg)
                return B;
            else
                return A;
        }
    }
}

void heapify (tSenha* V, int T, int i)
{
    int P = i;
    int E = esquerdo(i);
    int D = direito(i);
    
    if (E < T)
    {
        if ( (idoso(V[P]) && idoso(V[E])) || (!idoso(V[P]) && !idoso(V[E])) )
            P = menorTempo_de_Chegada(V, P, E);
        else if (idoso(V[E]))
            P = E;
    }
    
    if (D < T)
    {
        if ( (idoso(V[P]) && idoso(V[D])) || (!idoso(V[P]) && !idoso(V[D])) )
            P = menorTempo_de_Chegada(V, P, D);
        else if (idoso(V[D]))
            P = D;
    }
    
    if (P != i)
    {
        troca(V, P, i);
        heapify(V, T, P);
    }
}

void construirPrioridade (tSenha* V, int nSenhas)
{
    int T = nSenhas-1; //Indíce do último nó.
    int N = ((T-2)/2); //Indíce do último nó com filhos.
    for (int i = N; i >= 0; i--)
        heapify(V, nSenhas, i);
}

void lerOrgao(FILE* input, tOrgao* orgao)
{
    //Ler ID e n. de atendentes do orgão
    fscanf(input, "%s%*c%i%*c", orgao->id, &orgao->nAtendentes);
    orgao->vAtendente = (tAtendente*)malloc(sizeof(tAtendente)*orgao->nAtendentes);
    orgao->vSenha = (tSenha*)malloc(sizeof(tSenha)*capInicial);
    orgao->capSenhas = capInicial;
    orgao->nSenhas = 0;
}

void lerSenha(FILE* input, tSenha* temp)
{
    int i = 0;
    char c = 0;
    while (c != ':')
    {
        fscanf(input, "%c", &c);
        temp->orgao_desejado[i] = c;
        i++;
    }
    temp->orgao_desejado[i-1] = '\0';
    
    i = 0;
    c = 0;
    while (c != '-')
    {
        fscanf(input, "%c", &c);
        temp->nome[i] = c;
        i++;
    }
    temp->nome[i-1] = '\0';
    
    fscanf(input, "%i%*c", &temp->idade);
    
    fscanf(input, "%u%*c%u%*c%u%*c", &temp->tempo.hr, &temp->tempo.min, &temp->tempo.seg);
}

void verificarEspaco(tOrgao* O)
{
    if (O->nSenhas == O->capSenhas)
    {
        O->capSenhas = 2 * O->capSenhas;
        O->vSenha = (tSenha*)realloc(O->vSenha, sizeof(tSenha) * O->capSenhas);
    }
}

void inserirSenha(tSenha* senha, tOrgao* vOrgao, int nOrgaos)
{
    for (int i = 0; i < nOrgaos; i++)
    {
        if (strcmp(senha->orgao_desejado, vOrgao[i].id) == 0)
        {
            verificarEspaco(&vOrgao[i]);
            vOrgao[i].vSenha[vOrgao[i].nSenhas] = *senha;
            vOrgao[i].nSenhas++;
            break;
        }
    }
}

void removerSenha(tSenha* V, int* nSenhas, int* totSenhas)
{
    V[0] = V[*nSenhas-1]; //Inserir últ elemento na primeira posição
    (*nSenhas)--; //Decrementar senhas do órgão
    (*totSenhas)--; //Decrementar senhas geral
    heapify(V, *nSenhas, 0); //Repriorizar fila
}

void executarAtendimento(tOrgao* O, int* nSenhas)
{
    for (int i = 0; i < O->nAtendentes; i++)
    {
        if (O->nSenhas == 0)
        {
            O->nAtendentes = i;
            break;
        }
        
        strcpy(O->vAtendente[i].cliente, O->vSenha[0].nome); //Passar próxima senha para a atendente
        removerSenha(O->vSenha, &O->nSenhas, nSenhas); //Remover essa senha da lista
    }
}

void imprimirAtendentes(FILE* output, char* ID, tAtendente* V, int nAtendentes)
{
    if (nAtendentes == 0)
        return;
    
    fprintf(output, "[%s] ", ID);
    for (int i = 0; i < nAtendentes; i++)
    {
        if (i == nAtendentes-1)
            fprintf(output, "%s ", V[i].cliente);
        else
            fprintf(output, "%s, ", V[i].cliente);
    }
    fprintf(output, "\n");
}