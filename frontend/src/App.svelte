<script>
  import { onDestroy } from 'svelte';
  import AnalysisForm from './components/AnalysisForm.svelte';
  import StatusDisplay from './components/StatusDisplay.svelte';
  import ResultsDisplay from './components/ResultsDisplay.svelte';
  import { analyzeAddress, getWorkflowStatus, downloadReport } from './lib/api.js';

  let workflowId = null;
  let status = null;
  let results = null;
  let error = null;
  let statusInterval = null;

  const handleAnalyze = async (address) => {
    try {
      error = null;
      workflowId = null;
      status = null;
      results = null;

      const response = await analyzeAddress(address);
      workflowId = response.workflow_id;

      // Start polling for status
      startStatusPolling();
    } catch (err) {
      error = err.response?.data?.detail || err.message || 'Erreur lors du lancement de l\'analyse';
      console.error('Error analyzing address:', err);
    }
  };

  const startStatusPolling = () => {
    if (statusInterval) {
      clearInterval(statusInterval);
    }

    statusInterval = setInterval(async () => {
      if (!workflowId) return;

      try {
        const statusData = await getWorkflowStatus(workflowId);
        status = statusData;

        if (statusData.results) {
          results = statusData.results;
        }

        // Stop polling if completed or failed
        if (statusData.status === 'completed' || statusData.status === 'failed') {
          clearInterval(statusInterval);
          statusInterval = null;
        }
      } catch (err) {
        console.error('Error fetching status:', err);
        clearInterval(statusInterval);
        statusInterval = null;
      }
    }, 2000); // Poll every 2 seconds
  };

  const handleDownloadReport = async () => {
    if (!workflowId) return;

    try {
      const blob = await downloadReport(workflowId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `rapport_${workflowId}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      error = err.response?.data?.detail || err.message || 'Erreur lors du téléchargement du rapport';
      console.error('Error downloading report:', err);
    }
  };

  // Cleanup on component destroy
  onDestroy(() => {
    if (statusInterval) {
      clearInterval(statusInterval);
    }
  });
</script>

<main class="min-h-screen bg-gray-100 py-8">
  <div class="container mx-auto px-4">
    <header class="text-center mb-8">
      <h1 class="text-4xl font-bold text-gray-800 mb-2">AgentImmo</h1>
      <p class="text-gray-600">Analyse de pertinence d'emplacement pour projets immobiliers</p>
    </header>

    {#if error}
      <div class="max-w-md mx-auto mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <p class="font-bold">Erreur:</p>
        <p>{error}</p>
      </div>
    {/if}

    <AnalysisForm onSubmit={handleAnalyze} />

    {#if status}
      <StatusDisplay {status} />
    {/if}

    {#if results && status?.status === 'completed'}
      <ResultsDisplay {results} onDownloadReport={handleDownloadReport} />
    {/if}
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
  }
</style>

