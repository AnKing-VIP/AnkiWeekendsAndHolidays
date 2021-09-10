function setup(options) {
  const store = options.auxData();
  const boolInput = document.getElementById("weekends_and_holidays_cb");

  // update html when state changes
  store.subscribe((data) => {
    boolInput.checked = data["weekends_disabled"];
  });

  // update config when check state changes
  boolInput.addEventListener("change", (_) =>
    store.update((data) => {
      return { ...data, weekends_disabled: boolInput.checked };
    })
  );
}

$deckOptions.then((options) => {
  options.addHtmlAddon(HTML_CONTENT, () => setup(options));
});
