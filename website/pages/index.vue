<template>
  <div class="home">
    <section class="banner">
      <h1>BAIX accelerates bioinformatics</h1>
      <h2>medical research</h2>
      <p>Make medical research more accurate, efficient and easy</p>
      <button>Jion us</button>
    </section>
    <section class="process">
      <h2>Registration process</h2>
      <div class="linear"></div>
      <div>
        1100px

      </div>

    </section>
    <section class="source">
      <h2>Data Sources</h2>
      <div class="linear"></div>
      <div>
        1300px

      </div>
    </section>
    <section class="presentation">
      <h2>Case presentation</h2>
      <div class="linear"></div>
      <div>
        1300px

      </div>
    </section>
  </div>
</template>

<style lang="scss">

.home {
  .banner {
    height: 1080px;
    background-image: url('/bg.png');
    color: #ffffff;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .process {
    height: 1100px;
    text-align: center;
    h2 {
      font-size: 3rem;
    }
  }
  .source {
    height: 1300px;
    text-align: center;
    background-color: #C8E6C9;
    h2 {
      font-size: 3rem;
    }
  }
  .presentation {
    height: 1300px;
    text-align: center;
    h2 {
      font-size: 3rem;
    }
  }
}
</style>
