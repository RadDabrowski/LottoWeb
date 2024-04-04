document.addEventListener("DOMContentLoaded", function() {
    const showMoreButton = document.getElementById("showMore");
    const lottoToShow = document.querySelectorAll(".lotto-result");
    const eurojackpotToShow = document.querySelectorAll(".eurojackpot-result");
    let page = 1;
    const resultsPerPage = 10;

    lottoToShow.forEach(result => {
        result.style.display = "none";
    });
    eurojackpotToShow.forEach(result => {
        result.style.display = "none";
    });

    for (let i = 0; i < resultsPerPage && i < lottoToShow.length; i++) {
        lottoToShow[i].style.display = "block";
    }

    for (let i = 0; i < resultsPerPage && i < eurojackpotToShow.length; i++) {
        eurojackpotToShow[i].style.display = "block";
    }

    showMoreButton.addEventListener("click", function() {
        page++;
        const startIndex = (page - 1) * resultsPerPage;
        const endIndex = page * resultsPerPage;

        for (let i = startIndex; i < endIndex && i < lottoToShow.length; i++) {
            lottoToShow[i].style.display = "block";
        }

        for (let i = startIndex; i < endIndex && i < eurojackpotToShow.length; i++) {
            eurojackpotToShow[i].style.display = "block";
        }

        if (endIndex >= lottoToShow.length && endIndex >= eurojackpotToShow.length) {
            showMoreButton.disabled = true;
        }
    });
});