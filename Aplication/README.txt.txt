O experimento foi realizado da seguinte forma:

 - Foram realizado 12 Experimentos para avaliar a precisao da classificaçao dos gestos de mao.
 - Todos os experimentos foram conduzidos com o mesmo ambiente e iluminacao.
 - Para cada experimento, foram coletadas 2000 amostras realizando movimentos aleatorios utilizando apenas 1 gesto.
 - A cada amostra, foi salva em uma linha de um documento .csv
 - O nome do arquivo .csv segue a seguinte notaçao, (<mao><gesto>.csv)
 - a primeira linha do arquivo é o header, e indica o que representa cada coluna, nomeadamente (hand, gesture, position, orientation)
 - Foi entao mensurado para cada arquivo quantos % de acerto e quais sao os erros mais comuns para determinado gesto.


ToDo.

 - Melhorar o setup de testes:
	- utilizar um manipulador e realizar uma trajetoria com a mao anexada;	
	- comparar a posicao
	- Fazer uma rota, e verificar quantas amostras sao captadas para cada gesto de acordo com esta mesma rota
	- analisar os erros de classificacao dos gestos.
	
