// =========================================================================
// SCRIPT DA EDGE FUNCTION: analisar-prato
// Copie isso e cole no editor de código da Edge Function no Supabase
// =========================================================================

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

Deno.serve(async (req) => {
  // Tratar o "preflight request" que os navegadores fazem (CORS)
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const body = await req.json();
    const base64_image = body.base64_image;

    if (!base64_image) {
      return new Response(JSON.stringify({ error: "Nenhuma imagem foi recebida pelo servidor." }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 400,
      })
    }

    // A chave do Gemini deve estar configurada no painel "Edge Functions -> Secrets"
    const apiKey = Deno.env.get('GEMINI_API_KEY');
    if (!apiKey) {
      throw new Error("A chave secreta GEMINI_API_KEY não foi configurada no Supabase.");
    }

    // Remove a string técnica "data:image/jpeg;base64," do início da imagem
    const base64Data = base64_image.replace(/^data:image\/(png|jpeg|jpg|webp);base64,/, "");

    // Consulta à Inteligência Artificial Google Gemini 1.5 Flash (super rápido e voltado para visão)
    const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
    
    const geminiBody = {
      contents: [{
        parts: [
          { text: "Você é um nutricionista esportivo de alta performance. Analise esta foto de refeição e estime as calorias totais e os macronutrientes (Proteínas, Carboidratos e Gorduras). Seja super direto, responda APENAS com a lista nutricional e uma breve citação dos ingredientes que você detectou na imagem." },
          { inline_data: { mime_type: "image/jpeg", data: base64Data } }
        ]
      }]
    };

    const geminiResponse = await fetch(geminiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(geminiBody)
    });

    const geminiData = await geminiResponse.json();

    if (!geminiResponse.ok) {
      console.error(geminiData);
      throw new Error("Erro de comunicação com a API do Google Gemini.");
    }

    // Pegando a resposta textual do Nutricionista IA
    const aiText = geminiData.candidates[0].content.parts[0].text;

    // Retornando para a tela do seu celular!
    return new Response(
      JSON.stringify({ result: aiText }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    )
  }
})
