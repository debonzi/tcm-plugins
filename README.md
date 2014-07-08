TCM Backend Plugins
====================

TCM Core
--------

O core do TCM será apenas responsável pelo gerenciamento de informações comuns e necessárias para gerenciamento de contratos para os produtos titans, como usuário, produto, pacote, datas de criação, ativação, cancelamento, etc.
Em pontos chaves do gerenciamento do contrato serão enviados sinais (signals) para notificar possíveis módulos que necessitem gerar novas ações e armazenar informações extras, como ativações de serviços em sistemas terceiros (ex: SMT).

Sistema de sinais
-----------------

Para geração de sinais (TCM Core) e captura e execução de ações a sinais enviados (Backend plugins) será utilizada a biblioteca 'blinker'. Dessa maneira, podemos 'instrumentar' o core do TCM para enviar sinais para várias ações, que podem ou não ser relevantes aos plugins. Isso permite que cada plugin descida quais os sinais que são relevantes para manter a integridade das informações do backend ao qual faz interface.

Estrura e implementação
-----------------------

Dentro do diretório tcm foi criado um sub-diretório *backends* que contém as implementações dos backends plugins e alguns arquivos com funções do *sistema* de plugins.

**backends/__init__.py**: Contém a lista de plugins *instalados* e funções *utils* ao sistema de plugins. Um exemplo é a funçãos *get_pbe_info* (get payment-backend information) que busca o plugin do backend e caso exista, verifique se este implementa uma função que fornecesse *metadados* do backend e caso este implemente, retorna o informação. Funções auxiliares como essa podem ser implementadas para expor possíveis implementações dos backends, que podem ou não implementa-las.

A chamada da funções *get_pbe_info* está no modelo do contract (que pertence ao TCM Core). Caso o pluggin para o *payment-backend* não existe ou ainda não implemente essa função, apenas as informações básicas do contrato (gerenciadas pelo core) serão apresentadas:

<pre>
    def __iter__(self):
        yield 'name', self.name
        yield 'active', self.active
        yield 'activated', self.activated
        backend_info_f = get_pbe_info(self.backend)
        if callable(backend_info_f):
            yield 'backend', backend_info_f(self)
        else:
            yield 'backend', self.backend
</pre>

**backends/decorators.py**: Implementa o decorador *@backend_handler* que verifica se o signal pertence ao backend e só executa o handler em caso positivo.

**backends/smt/__init__.py**: Implementa os handlers e *assina* os signals de interesse. Nesse caso, são criados *handlers* para a criação e cancelamento do contrato.

<pre>
@backend_handler
def created(sender, backend):
    sender.activated = True
    print "\tSMT handles %s creation" %sender.name
 
@backend_handler
def cancelled(sender, backend):
    sender.activated = False
    print "\tSMT handles %s cancel" %sender.name

signal('on_contract_create').connect(created)
signal('on_contract_cancel').connect(cancelled)
</pre>

No caso, *sender* é um objecto Contract.

**backends/smt/models.py**: Idealmente implementaria o(s) model(s) do backend SMT, mas apenas para efeito de demonstração e ensaio, este implementa a função *get_model_repr*, que é utilizada pelo *get_pbe_info*.

**main.py**: Implementa casos básicos de contratos. Os campos são minimos e *hardcoded*.
O *classmethod* Contract.create_contract recebe os paramentros *name* e *backend*, que no caso real seria representado pelo Contract.Product.payment_backend.

No processo __main__ serão criados 3 contratos:

 * Contract_1 com backend `smt`, o qual está implementado, implementa handlers para create e cancel (imprime mensagem e seta activated=True e activated=False respectivamente) e implementa função para gerar a representação do modelo.
 * Contract_2 com backend `telmex`, o qual está implementado e implementa handlers para create a cancel (apenas imprime mensagens).
 * Contract_3 com backend `net`, o qual não possui backend.

A saida da função __main__ é:

<pre>
#########################################################
contract Contract_1 will be created
	SMT handles Contract_1 creation ## *--Impresso pelo handler de criação
Contract Contract_1 created

{
  "active": true, 
  "activated": true, ## *-- Setada pelo backend plugin
  "name": "Contract_1", 
  "backend": {                      ##
    "name": "smt",                  ## *-- fornecida pelo backend plugin
    "contract": "Contract_1"        ##
  }
}
Contract Contract_1 is about to be cancelled
	SMT handles Contract_1 cancel   ## *-- Impresso pelo handler de cancelamento
Contract Contract_1 cancelled

{
  "active": false, 
  "activated": false,               ## *-- Anulada pelo backend plugin
  "name": "Contract_1", 
  "backend": {
    "name": "smt", 
    "contract": "Contract_1"
  }
}
#########################################################

#########################################################
contract Contract_2 will be created
	TELMEX handles Contract_2 creation  ## *-- Impresso pelo handler de criação
Contract Contract_2 created

{
  "active": true, 
  "activated": false, 
  "name": "Contract_2", 
  "backend": "telmex"                   ## *-- Não possui representação fornecida pelo backend plugin
}
Contract Contract_2 is about to be cancelled
	TELMEX handles Contract_2 cancel   ## *- Impresso pelo handler de cancelamento
Contract Contract_2 cancelled

{
  "active": false, 
  "activated": false, 
  "name": "Contract_2", 
  "backend": "telmex"
}
#########################################################

#########################################################
contract Contract_3 will be created            ## *-|
Contract Contract_3 created                    ## *-- Não possui handler

{
  "active": true, 
  "activated": false, 
  "name": "Contract_3", 
  "backend": "net" ## *-- Não possui representação fornecida pelo backend plugin
}
Contract Contract_3 is about to be cancelled ## *-|
Contract Contract_3 cancelled                ## *-- Não possui handler

{
  "active": false, 
  "activated": false, 
  "name": "Contract_3", 
  "backend": "net"
}
#########################################################
</pre>
