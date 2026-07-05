> **Contexto:** Transposição da ilustração vetorial (conjunto de blocos retangulares do "Grupo 3" do Figma) para o front-end real do projeto, utilizando posicionamento absoluto responsivo.

Abaixo, encontram-se compiladas as instruções exatas de onde e como aplicar os trechos desenvolvidos:

### 1. Estrutura de Marcação (Onde inserir no HTML)

O bloco estrutural abaixo deve ser posicionado de forma cirúrgica na página do curso: **imediatamente após o fechamento da tag do seu menu/header (`</nav>` ou `</header>`)** e logo antes do container principal que inicia a listagem dos módulos.

```html
<section class="decorative-blocks" aria-hidden="true">
  <span class="decorative-block decorative-block--outline block-01"></span>
  <span class="decorative-block decorative-block--outline block-02"></span>

  <span class="decorative-block decorative-block--filled block-03"></span>
  <span class="decorative-block decorative-block--filled block-04"></span>
  <span class="decorative-block decorative-block--outline block-05"></span>
  <span class="decorative-block decorative-block--filled block-06"></span>

  <span class="decorative-block decorative-block--filled block-07"></span>
  <span class="decorative-block decorative-block--filled block-08"></span>
  <span class="decorative-block decorative-block--outline block-09"></span>
</section>

```

### 2. Estilização e Responsividade (Onde adicionar no CSS)

Estas regras devem ser anexadas ao final do seu arquivo de estilos principal (como `global.css` ou `styles.css`). Elas garantem o posicionamento em pixels mapeado do Figma e tratam o comportamento adaptativo para telas menores de até 900px (ocultando os blocos excedentes para evitar quebra de layout):

```css
/* ==========================================================================
   ILUSTRAÇÃO DE BLOCOS RETANGULARES (FIGMA - GRUPO 3)
   ========================================================================== */

.decorative-blocks {
  position: relative;
  width: 100%;
  min-height: 500px;
  overflow: hidden;
  pointer-events: none; /* Garante que os blocos não atrapalhem cliques na página */
}

.decorative-block {
  position: absolute;
  width: 120px;
  height: 120px;
  display: block;
}

.decorative-block--filled {
  background-color: #5fbd7b;
}

.decorative-block--outline {
  border: 8px solid #5fbd7b;
  background-color: transparent;
}

/* Distribuição Espacial dos Blocos (Telas Grandes) */
.block-01 { left: 16%; top: 270px; }
.block-02 { left: 35%; top: 135px; }

/* Fileira superior à direita */
.block-03 { left: 55%; top: 0; }
.block-04 { left: 67%; top: 0; }
.block-05 { left: 78.5%; top: 0; }
.block-06 { left: 89.5%; top: 0; }

/* Blocos intermediários e inferiores */
.block-07 { left: 55%; top: 135px; }
.block-08 { left: 66%; top: 270px; }
.block-09 { left: 82%; top: 270px; }

/* Comportamento em Telas Menores (Até 900px) */
@media (max-width: 900px) {
  .decorative-blocks {
    min-height: 360px;
  }

  .decorative-block {
    width: 80px;
    height: 80px;
  }

  .decorative-block--outline {
    border-width: 6px;
  }

  .block-01 { left: 8%; top: 220px; }
  .block-02 { left: 34%; top: 115px; }
  .block-03 { left: 58%; top: 0; }
  .block-04 { left: 72%; top: 0; }
  .block-07 { left: 58%; top: 100px; }
  .block-08 { left: 72%; top: 210px; }

  /* Oculta blocos periféricos para preservar o espaço em telas menores */
  .block-05,
  .block-06,
  .block-09 {
    display: none;
  }
}

```