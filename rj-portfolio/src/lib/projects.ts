import { supabase } from '@/lib/supabase';

export interface Project {
    id: number;
    title: string;
    slug: string;
    description: string;
    tech_stack: string[];
    link_url?: string;
    github_url?: string;
    demo_url?: string;
    image_url?: string;
    featured: boolean;
}

export async function getFeaturedProjects(): Promise<Project[]> {
    const { data, error } = await supabase
        .from('projects')
        .select('*')
        .eq('featured', true)
        .order('id', { ascending: true });

    if (error) {
        console.error('Error fetching projects:', error);
        return [];
    }

    return data as Project[];
}