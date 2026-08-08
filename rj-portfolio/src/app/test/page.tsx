import { supabase } from '@/lib/supabase';

export default async function TestPage() {
    const { data, error } = await supabase.from('projects').select('*');

    return (
        <main className="p-10">
            <h1 className="text-3xl font-bold">Supabase Test</h1>

            {error && (
                <pre className="text-red-600">
                    {JSON.stringify(error, null, 2)}
                </pre>
            )}

            <pre className="mt-6 rounded bg-gray-100 p-4 text-sm">
                {JSON.stringify(data, null, 2)}
            </pre>
        </main>
    );
}