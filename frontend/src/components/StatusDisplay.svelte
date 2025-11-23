<script>
  export let status = null;

  const statusLabels = {
    pending: 'En attente',
    collecting: 'Collecte des données',
    analyzing: 'Analyse en cours',
    visualizing: 'Génération des visualisations',
    building_report: 'Création du rapport',
    completed: 'Terminé',
    failed: 'Échec',
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-gray-500',
      collecting: 'bg-blue-500',
      analyzing: 'bg-yellow-500',
      visualizing: 'bg-purple-500',
      building_report: 'bg-indigo-500',
      completed: 'bg-green-500',
      failed: 'bg-red-500',
    };
    return colors[status] || 'bg-gray-500';
  };
</script>

{#if status}
  <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
    <h2 class="text-xl font-bold mb-4">État de l'analyse</h2>
    <div class="mb-4">
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-medium text-gray-700">
          {statusLabels[status.status] || status.status}
        </span>
        <span class="text-sm text-gray-500">
          {Math.round(status.progress * 100)}%
        </span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2.5">
        <div
          class="h-2.5 rounded-full {getStatusColor(status.status)}"
          style="width: {status.progress * 100}%"
        ></div>
      </div>
    </div>
    {#if status.error}
      <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <p class="font-bold">Erreur:</p>
        <p>{status.error}</p>
      </div>
    {/if}
  </div>
{/if}






