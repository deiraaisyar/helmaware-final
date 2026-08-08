import Container from '@/components/common/Container';
import ProjectCard from '@/components/common/ProjectCard';
import FadeInSection from '@/components/common/FadeInSection';
import { supabase } from '@/lib/supabase';

interface ProjectsSectionProps {
    locale: string;
    dict: {
        subtitle: string;
        title: string;
        description: string;
    };
}

export default async function ProjectsSection({
    locale,
    dict,
}: ProjectsSectionProps) {
    const { data: projects, error } = await supabase
        .from('projects')
        .select('*')
        .order('id', { ascending: true });

    if (error) console.error(error);

    return (
        <section id="projects" className="bg-[#F8F7F4] py-28">
            <FadeInSection>
                <Container>
                    <div className="mb-14 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
                        <div>
                            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#C56E3D]">
                                {dict.subtitle}
                            </p>
                            <h2 className="mt-3 text-4xl font-bold text-[#1F2937] md:text-5xl">
                                {dict.title}
                            </h2>
                        </div>

                        <p className="max-w-md text-base leading-relaxed text-[#6B7280]">
                            {dict.description}
                        </p>
                    </div>

                    {!projects || projects.length === 0 ? (
                        <div className="rounded-3xl border border-[#E7E2DA] bg-white p-10 text-center text-[#6B7280]">
                            {locale === 'id'
                                ? 'Belum ada proyek yang tersedia.'
                                : 'No projects available yet.'}
                        </div>
                    ) : (
                        <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
                            {projects.map((project: any) => (
                                <ProjectCard
                                    key={project.id}
                                    title={locale === 'id' ? project.title_id : project.title_en}
                                    description={
                                        locale === 'id'
                                            ? project.description_id
                                            : project.description_en
                                    }
                                    tags={project.tech_stack}
                                    time={project.time}
                                    type={project.type}
                                    slug={project.slug}
                                    image_url={project.image_url}
                                    locale={locale}
                                />
                            ))}
                        </div>
                    )}
                </Container>
            </FadeInSection>
        </section>
    );
}
