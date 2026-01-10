<script>
  import { onDestroy } from 'svelte';
  import { link } from 'svelte-spa-router';
  import AnalysisForm from '../components/AnalysisForm.svelte';
  import StatusDisplay from '../components/StatusDisplay.svelte';
  import ResultsDisplay from '../components/ResultsDisplay.svelte';
  import { analyzeAddress, getWorkflowStatus, downloadReport } from '../lib/api.js';

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

<div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
  <!-- Navigation -->
  <nav class="border-b border-slate-700/50 backdrop-blur-sm bg-slate-900/50 sticky top-0 z-50">
    <div class="container mx-auto px-6 py-4">
      <div class="flex items-center justify-between">
        <a href="/" use:link class="flex items-center gap-3 group">
          <div class="w-10 h-10 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/20 group-hover:shadow-cyan-500/40 transition-shadow">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
            </svg>
          </div>
          <span class="text-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">AgentImmo</span>
        </a>
        <div class="flex items-center gap-4">
          <a href="/city-information" use:link class="px-4 py-2 text-sm font-medium text-slate-300 hover:text-cyan-400 transition-colors flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
            </svg>
            City Information
          </a>
        </div>
      </div>
    </div>
  </nav>

  <main class="container mx-auto px-6 py-12">
    <!-- Header -->
    <header class="text-center mb-12">
      <h1 class="text-4xl md:text-5xl font-bold text-white mb-4">
        <span class="bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
          AgentImmo
        </span>
      </h1>
      <p class="text-slate-400 text-lg max-w-2xl mx-auto">
        Analyse de pertinence d'emplacement pour projets immobiliers
      </p>
    </header>

    {#if error}
      <div class="max-w-md mx-auto mb-8">
        <div class="bg-red-500/10 border border-red-500/30 rounded-xl p-5 flex items-start gap-4">
          <div class="flex-shrink-0 w-10 h-10 bg-red-500/20 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
          </div>
          <div>
            <h3 class="text-red-400 font-semibold mb-1">Erreur</h3>
            <p class="text-red-300/80">{error}</p>
          </div>
        </div>
      </div>
    {/if}

    <AnalysisForm onSubmit={handleAnalyze} />

    {#if status}
      <StatusDisplay {status} />
    {/if}

    {#if results && status?.status === 'completed'}
      <ResultsDisplay {results} onDownloadReport={handleDownloadReport} />
    {/if}

    <!-- Features Section -->
    <section class="mt-16 grid md:grid-cols-3 gap-6">
      <a href="/city-information" use:link class="group p-6 bg-slate-800/50 rounded-2xl border border-slate-700/50 hover:border-cyan-500/30 transition-all duration-300">
        <div class="w-12 h-12 bg-cyan-500/20 rounded-xl flex items-center justify-center mb-4 group-hover:bg-cyan-500/30 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-cyan-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-white mb-2">City Information</h3>
        <p class="text-slate-400 text-sm">Obtenez des informations détaillées sur n'importe quelle ville française.</p>
      </a>

      <div class="p-6 bg-slate-800/50 rounded-2xl border border-slate-700/50 opacity-60">
        <div class="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-400" viewBox="0 0 20 20" fill="currentColor">
            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-white mb-2">Analyse de Marché</h3>
        <p class="text-slate-400 text-sm">Analyse DVF et données cadastrales (bientôt disponible).</p>
      </div>

      <div class="p-6 bg-slate-800/50 rounded-2xl border border-slate-700/50 opacity-60">
        <div class="w-12 h-12 bg-emerald-500/20 rounded-xl flex items-center justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm2 10a1 1 0 10-2 0v3a1 1 0 102 0v-3zm2-3a1 1 0 011 1v5a1 1 0 11-2 0v-5a1 1 0 011-1zm4-1a1 1 0 10-2 0v7a1 1 0 102 0V8z" clip-rule="evenodd" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-white mb-2">Rapport PDF</h3>
        <p class="text-slate-400 text-sm">Génération automatique de rapports professionnels (bientôt disponible).</p>
      </div>
    </section>
  </main>
</div>

<style>
  :global(body) {
    margin: 0;
  }
</style>


