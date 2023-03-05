<template>
  <div class="home">
    <section class="banner">
      <h1>BAIX accelerates bioinformatics</h1>
      <h2>medical research</h2>
      <p>Make medical research more accurate, efficient and easy</p>
      <a href="http://graph.baix.ai/register" target="_blank">Jion us</a>
    </section>
    <section class="process">
      <div class="container">
        <h2>Registration process</h2>
        <div class="linear"></div>
        <div class="process-content">
          <div class="process-item">
            <div class="process-part">Part 1</div>
            <div class="process-name">
              <div>Register</div>
              <span></span>
              <i>
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 12L24 24L12 36" stroke="#03b150" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M24 12L36 24L24 36" stroke="#03b150" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </i>
            </div>
            <div class="process-icon part-1"></div>
            <div class="process-desc">Fill in keywords</div>
          </div>
          <div class="process-item">
            <div class="process-part">Part 2</div>
            <div class="process-name">
              <div>Review</div>
              <span></span>
              <i>
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 12L24 24L12 36" stroke="#03b150" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M24 12L36 24L24 36" stroke="#03b150" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </i>
            </div>
            <div class="process-icon part-2"></div>
            <div class="process-desc">After reviewing the email, <br /> Activate function</div>
          </div>
          <div class="process-item">
            <div class="process-part">Part 3</div>
            <div class="process-name">
              <div>Use</div>
              <span></span>
            </div>
            <div class="process-icon part-3"></div>
            <div class="process-desc">Using BAIX, <br />Accelerate scientific research</div>
          </div>
        </div>
      </div>
    </section>
    <section class="source">
      <div class="container">
        <h2>Data Sources</h2>
        <div class="linear"></div>
        <div class="source-content">
          <div class="source-item left">
            <div class="source-heavy align-right">~1400 <span style="font-size: 2.5rem;"> W</span></div>
            <div style="padding-top: 16rem;">
              <div class="source-heavy align-left">~100 <span style="font-size: 2.5rem;"> W</span></div>
              <div class="source-title">Program</div>
              <ol class=" align-left">
                <li>BAIX</li>
                <li>BX-Medical SaaS Platform</li>
              </ol>
            </div>
          </div>
          <div class="source-item right">
            <div>
              <div class="source-title">Knowledge graph</div>
              <ol>
                <li>More than 14 million SCI medical documents</li>
                <li>knowledge map graph structure storage</li>
                <li>Automatic labeling</li>
              </ol>
            </div>
            <div style="padding-top: 4rem;">
              <div class="source-heavy align-right">12 <span style="font-size: 2.5rem;"> PB</span></div>
              <div class="source-title">Genetic Drug Data</div>
              <ol>
                <li>KEGG database</li>
                <li>Drugbank</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="presentation">
      <div class="container">
        <h2>Case presentation</h2>
        <div class="linear"></div>
        <div class="presentation-content">
          <div class="presentation-item">
            <div class="presentation-title">
              <div>PPT generation</div>
              <span></span>
            </div>
            <div class="presentation-img"><img src="/ppt1.png" /></div>
            <div class="presentation-img"><img src="/ppt2.png" /></div>
          </div>
          <div class="presentation-item">
            <div class="presentation-title">
              <div>Table recognition</div>
              <span></span>
            </div>
            <div class="presentation-img"><img src="/table1.png" /></div>
            <div class="presentation-img"><img src="/table2.png" /></div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style lang="scss">

.home {
  .banner {
    height: 1080px;
    background-image: url('/bg-light.png');
    background-size: cover;
    background-repeat: no-repeat;
    color: #ffffff;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    // justify-content: center;
    padding-top: 15rem;

    h1, h2 {
      font-size: 3.5rem;
      font-weight: normal;
    }
    p {
      padding-top: 2rem;
      margin-bottom: 3rem;
      font-size: 2rem;
    }
    a {
      background-color: var(--color-primary);
      color: #FFFFFF;
      padding: 1rem 3.5rem;
      font-size: 2rem;
      cursor: pointer;
    }
  }

  .process {
    // height: 1100px;
    text-align: center;
    padding: 0 10rem 10rem;
    h2 {
      font-size: 3rem;
      padding: 70px 0 40px;
    }

    .process-content {
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: stretch;
      padding-top: 5rem;
    }
    .process-item {
      // flex-grow: 1;
      flex: 1 0 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      // justify-content: center;
      position: relative;
    }
    .process-part {
      color: var(--color-primary);
      font-size: 2rem;
      padding-bottom: 2rem;
    }
    .process-icon {
      width: 244px;
      height: 240px;
      border-radius: 50%;
      // border: 2px solid var(--color-primary);
      background-position: center;
      background-size: auto;
      background-repeat: no-repeat;
      &.part-1 {
        background-image: url('/part1.png');
      }
      &.part-2 {
        background-image: url('/part2.png');
      }
      &.part-3 {
        background-image: url('/part3.png');
      }
    }
    .process-desc {
      font-size: 2rem;
      padding-top: 1rem;
    }
    .process-name {
      width: 100%;
      font-size: 2rem;
      padding-bottom: 1.5rem;
      border-bottom: 2px solid  var(--color-border);
      margin-bottom: 3rem;
      position: relative;
      span {
        display: block;
        width: 226px;
        border: 3px solid var(--color-primary);
        position: absolute;
        bottom: -4px;
        left: 50%;
        margin-left: -113px;
      }
      i {
        width: 48px;
        height: 48px;
        background-color: transparent;
        position: absolute;
        bottom: -25px;
        right: -25px;
        z-index: 99;
      }
    }
  }
  .source {
    // height: 1300px;
    text-align: center;
    background-color: #C8E6C9;
    padding: 0 10rem 10rem;

    background-color: #f2fbf6;
    h2 {
      font-size: 3rem;
      padding: 70px 0 40px;
    }
    .source-content {
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      padding-top: 5rem;
      background-position: center;
      background-size: auto;
      background-repeat: no-repeat;
      background-image: url('/source.png');
    }
    .source-item {
      // padding: 0 15rem;
      flex: 1 0 0;
      text-align: left;
      &.left {
        padding-right: 15rem;
        text-align: right;
      }
      &.right {
        padding-left: 15rem;
        text-align: left;
      }

      ol {
        list-style: unset;
        padding-left: 2rem;
      }
      li {
        font-size: 2rem;
      }
    }
    .source-heavy {
      font-size: 4rem;
      font-weight: 400;
      padding-bottom: 2rem;
    }
    .source-title {
      background-color:  var(--color-primary);
      width: 450px;
      height: 86px;
      line-height: 86px;
      text-align: center;
      color: #ffffff;
      font-size: 2rem;
    }
  }
  .presentation {
    // height: 1300px;
    text-align: center;
    padding: 0 10rem 10rem;
    h2 {
      font-size: 3rem;
      padding: 70px 0 40px;
    }
    .presentation-content {
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: stretch;
      padding-top: 5rem;
    }
    .presentation-item {
      flex: 1 0 0;
      text-align: left;
      padding: 0 2rem;
      width: 50%;
    }
    .presentation-title {
      color: var(--color-primary);
      font-size: 2rem;
      padding: 1rem 0;
      margin-bottom: 3rem;

      div {
        background-image: linear-gradient(to bottom, #03b150, #91d050);
        background-clip: text;
        color: transparent;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 4px;
      }
      span {
        width: 100%;
        height: 4px;
        display: block;
        background-image: linear-gradient(to right, #03b150, #91d050);
      }
    }
    .presentation-img {
      margin-top: 2rem;
      width: 100%;
      img {
        width: 100%;
      }
    }
  }
}
</style>
