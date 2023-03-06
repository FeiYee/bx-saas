<template>
  <div class="about">
    <section class="introduce">
      <div class="container">
        <h2>About BAIX</h2>
        <p>BAIX focuses on the Al analysis SaaS platform of clinical data, real world and medical science and technology literature, and we are committed to breaking the island of medical data.</p>

        <p>Through advanced Al innovation technologies such as machine learning, deep learning, and multimodal knowledge graphs, it can be effectively combined with medical clinical data, imaging data, real-world big data, and literature knowledge graphs to provide deeper, more comprehensive, and more accurate information for medical science and technology work. Al analysis helps pharmaceutical companies, doctors, and researchers conduct research on basic medicine and drug mechanisms. The existing analysis results have helped clients successfully publish nearly a hundred high-scoring SCI articles.</p>
      </div>
    </section>
    <section class="contact">
      <div class="container">
        <h2>Contact us</h2>
        <div class="linear"></div>
        <div class="contact-content">
          <div>
            <i>
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M24 44C24 44 39 32 39 19C39 10.7157 32.2843 4 24 4C15.7157 4 9 10.7157 9 19C9 32 24 44 24 44Z" fill="none" stroke="#b6b6b6" stroke-width="4" stroke-linejoin="round"/>
                <path d="M24 25C27.3137 25 30 22.3137 30 19C30 15.6863 27.3137 13 24 13C20.6863 13 18 15.6863 18 19C18 22.3137 20.6863 25 24 25Z" fill="none" stroke="#b6b6b6" stroke-width="4" stroke-linejoin="round"/>
              </svg>
            </i>
            No. 36, Haidian West Street, Belling, China</div>
          <div>
            <i>
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M24 44C24 44 39 32 39 19C39 10.7157 32.2843 4 24 4C15.7157 4 9 10.7157 9 19C9 32 24 44 24 44Z" fill="none" stroke="#b6b6b6" stroke-width="4" stroke-linejoin="round"/>
                <path d="M24 25C27.3137 25 30 22.3137 30 19C30 15.6863 27.3137 13 24 13C20.6863 13 18 15.6863 18 19C18 22.3137 20.6863 25 24 25Z" fill="none" stroke="#b6b6b6" stroke-width="4" stroke-linejoin="round"/>
              </svg>
            </i>
            19768 E 47th Dr, Denver, CO, US</div>
          <div>
            <i>
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M36 15H44V28V41H4V28V15H12" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M24 19V5" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M30 11L24 5L18 11" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 15L24 30L44 15" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </i>
            bd@aibaixh.com</div>
        </div>
      </div>
    </section>
  </div>
</template>
<style lang="scss">
.header {
  a {
    color: #333;
  }
}
.about {
  .introduce {
    // height: 8rem;
    padding: 0 1.8rem 0.8rem;
    padding-top: 1.6rem;
    background-image: url('/bg-light.png');
    background-color: rgba(255, 255, 255, 0.6);
    background-blend-mode: overlay;
    background-position: center;
    font-size: 0.28rem;
    color: #333;

    h2, p {
      margin-bottom: 0.46rem;

    }
  }
  .contact {
    height: 7rem;
    text-align: center;
    padding: 0.6rem 2rem 1.6rem;

    h2 {
      font-size: 0.42rem;
    }

    .contact-content {
      padding-top: 0.8rem;
      text-align: left;
      div {
        padding: 0.16rem 0;
        font-size: 0.32rem;
      }
      i {
        margin-right: 6px;
      }
      svg {
        width: 36px;
        height: 36px;
      }
    }
  }
}
</style>
