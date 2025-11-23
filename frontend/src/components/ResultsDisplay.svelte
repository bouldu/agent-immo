<script>
  export let results = null;
  export let onDownloadReport = null;

  const formatValue = (value) => {
    if (value === null || value === undefined) {
      return 'N/A';
    }
    if (typeof value === 'number') {
      return value.toLocaleString('fr-FR');
    }
    return value;
  };
</script>

{#if results}
  <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
    <h2 class="text-xl font-bold mb-4">Résultats de l'analyse</h2>

    {#if results.indicators}
      <div class="mb-6">
        <h3 class="text-lg font-semibold mb-3">Indicateurs</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          {#if results.indicators.prix_m2_moyen !== null}
            <div class="border rounded p-4">
              <p class="text-sm text-gray-600">Prix au m² moyen</p>
              <p class="text-2xl font-bold">
                {formatValue(results.indicators.prix_m2_moyen)} €/m²
              </p>
            </div>
          {/if}
          {#if results.indicators.prix_m2_median !== null}
            <div class="border rounded p-4">
              <p class="text-sm text-gray-600">Prix au m² médian</p>
              <p class="text-2xl font-bold">
                {formatValue(results.indicators.prix_m2_median)} €/m²
              </p>
            </div>
          {/if}
        </div>
      </div>
    {/if}

    {#if results.images}
      <div class="mb-6">
        <h3 class="text-lg font-semibold mb-3">Visualisations</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          {#if results.images.price_chart}
            <div class="border rounded p-4">
              <p class="text-sm text-gray-600 mb-2">Graphique des prix</p>
              <p class="text-xs text-gray-500">
                (Visualisation à implémenter)
              </p>
            </div>
          {/if}
          {#if results.images.trend_chart}
            <div class="border rounded p-4">
              <p class="text-sm text-gray-600 mb-2">Tendances du marché</p>
              <p class="text-xs text-gray-500">
                (Visualisation à implémenter)
              </p>
            </div>
          {/if}
        </div>
      </div>
    {/if}

    {#if onDownloadReport}
      <div class="mt-6">
        <button
          on:click={onDownloadReport}
          class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          Télécharger le rapport PDF
        </button>
      </div>
    {/if}
  </div>
{/if}






