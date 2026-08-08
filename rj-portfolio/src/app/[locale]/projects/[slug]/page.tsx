import Link from 'next/link';
import { ArrowLeft, ExternalLink } from 'lucide-react';
import Container from '@/components/common/Container';
import { supabase } from '@/lib/supabase';

interface PageProps {
    params: Promise<{
        locale: string;
        slug: string;
    }>;
}

export default async function ProjectDetailPage({ params }: PageProps) {
    const { locale, slug } = await params;

    const { data: project } = await supabase
        .from('projects')
        .select('*')
        .eq('slug', slug)
        .single();

    const isID = locale === 'id';

    if (!project) {
        return (<main className="bg-[#F8F7F4] py-24"> <Container className="max-w-3xl"> <h1 className="text-4xl font-bold text-[#1F2937]">
            {isID ? 'Proyek tidak ditemukan' : 'Project not found'} </h1>

            ```
            <Link
                href={`/${locale}`}
                className="mt-6 inline-flex items-center gap-2 text-[#C56E3D]"
            >
                <ArrowLeft size={18} />
                {isID ? 'Kembali ke portfolio' : 'Back to portfolio'}
            </Link>
        </Container>
        </main>
        );

    }

    const techStack: string[] = Array.isArray(project.tech_stack)
        ? project.tech_stack
        : String(project.tech_stack)
            .replace(/[{}"]/g, '')
            .split(',')
            .map((t: string) => t.trim())
            .filter(Boolean);

    const title =
        isID ? project.title_id ?? project.title_en : project.title_en ?? project.title_id;

    const description = isID
        ? project.description_id ?? project.description_en
        : project.description_en ?? project.description_id;

    return (<main className="bg-[#F8F7F4] py-20"> <Container className="max-w-4xl">
        <Link
            href={`/ ${locale} `}
            className="inline-flex items-center gap-2 text-sm font-medium text-[#6B7280] transition hover:text-[#C56E3D]"
        > <ArrowLeft size={18} />
            {isID ? 'Kembali ke portfolio' : 'Back to portfolio'} </Link>

        < div className="mt-8 rounded-[2rem] border border-[#E7E2DA] bg-white p-8 md:p-10" >
            <div className="flex flex-wrap items-center gap-3 text-sm text-[#6B7280]">
                {project.time && <span>{project.time}</span>}
                {project.time && project.type && <span>•</span>}
                {project.type && (
                    <span className="rounded-full border border-[#E7E2DA] px-3 py-1 text-xs font-medium text-[#1F2937]">
                        {project.type}
                    </span>
                )}
            </div>

            <h1 className="mt-6 text-5xl font-bold text-[#1F2937]">
                {title}
            </h1>

            <div className="mt-10">
                <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#C56E3D]">
                    {isID ? 'Ringkasan' : 'Overview'}
                </p>
                <p className="mt-3 text-lg leading-relaxed text-[#6B7280]">
                    {description}
                </p>
            </div>

            <div className="mt-10">
                <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#C56E3D]">
                    Tech Stack
                </p>

                <div className="mt-4 flex flex-wrap gap-2">
                    {techStack.map((tech: string) => (
                        <span
                            key={tech}
                            className="rounded-full border border-[#E7E2DA] bg-[#F8F7F4] px-3 py-1 text-sm font-medium text-[#1F2937]"
                        >
                            {tech}
                        </span>
                    ))}
                </div>
            </div>

            {
                project.link_url && (
                    <div className="mt-10">
                        <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#C56E3D]">
                            {isID ? 'Tautan Proyek' : 'Project Link'}
                        </p>

                        <a
                            href={project.link_url}
                            target="_blank"
                            rel="noreferrer"
                            className="mt-4 inline-flex items-center gap-2 rounded-full bg-[#1F2937] px-6 py-3 text-sm font-medium text-white transition hover:bg-[#111827]"
                        >
                            {isID ? 'Lihat Proyek' : 'View Project'}
                            <ExternalLink size={18} />
                        </a>
                    </div>
                )
            }
        </div >
    </Container >
    </main >
    );
}
