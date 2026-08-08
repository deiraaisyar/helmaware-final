import Container from '@/components/common/Container';
import FadeInSection from '@/components/common/FadeInSection';

interface NonITProjectsSectionProps {
    locale: string;
}

const projects = {
    en: [
        {
            title: 'On The Map by AIESEC in UGM',
            time: '2025',
            description:
                'Led event planning and cross-functional coordination for a community-driven program involving partnerships, budgeting, logistics, and participant experience.',
            tags: ['Leadership', 'Project Management', 'Partnership', 'Operations'],
        },
        {
            title: 'OmahTI Academy 2025',
            time: '2025',
            description:
                'Contributed to the development and execution of a large-scale technology education initiative, focusing on coordination, communication, and program operations.',
            tags: ['Community', 'Coordination', 'Education', 'Execution'],
        },
    ],
    id: [
        {
            title: 'On The Map by AIESEC in UGM',
            time: '2025',
            description:
                'Memimpin perencanaan acara dan koordinasi lintas divisi untuk program berbasis komunitas yang melibatkan kemitraan, penganggaran, logistik, dan pengalaman peserta.',
            tags: ['Kepemimpinan', 'Manajemen Proyek', 'Kemitraan', 'Operasional'],
        },
        {
            title: 'OmahTI Academy 2025',
            time: '2025',
            description:
                'Berkontribusi dalam pengembangan dan pelaksanaan inisiatif pendidikan teknologi berskala besar dengan fokus pada koordinasi, komunikasi, dan operasional program.',
            tags: ['Komunitas', 'Koordinasi', 'Edukasi', 'Eksekusi'],
        },
    ],
};

export default function NonITProjectsSection({
    locale,
}: NonITProjectsSectionProps) {
    const items = locale === 'id' ? projects.id : projects.en;

    return (<section id="non-it-projects" className="py-28"> <FadeInSection> <Container> <div className="mb-14"> <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#C56E3D]">
        {locale === 'id' ? 'Proyek Non-IT' : 'Non-IT Projects'} </p> <h2 className="mt-3 text-4xl font-bold text-[#1F2937] md:text-5xl">
            {locale === 'id'
                ? 'Kepemimpinan, Komunitas, & Eksekusi'
                : 'Leadership, Community, & Execution'} </h2> <p className="mt-4 max-w-2xl text-lg leading-relaxed text-[#6B7280]">
            {locale === 'id'
                ? 'Proyek dan inisiatif di luar bidang teknis yang membentuk kemampuan kepemimpinan, kolaborasi, manajemen proyek, dan eksekusi.'
                : 'Projects and initiatives beyond technical development that shaped leadership, collaboration, project management, and execution skills.'} </p> </div>
        <div className="grid gap-6 md:grid-cols-2">
            {items.map((project) => (
                <div
                    key={project.title}
                    className="rounded-3xl border border-[#E7E2DA] bg-white p-6 transition hover:border-[#C56E3D] hover:shadow-[0_18px_40px_rgba(31,41,55,0.08)]"
                >
                    <div className="flex items-center justify-between">
                        <h3 className="text-2xl font-semibold text-[#1F2937]">
                            {project.title}
                        </h3>
                        <span className="text-sm text-[#6B7280]">{project.time}</span>
                    </div>

                    <p className="mt-4 text-base leading-relaxed text-[#6B7280]">
                        {project.description}
                    </p>

                    <div className="mt-6 flex flex-wrap gap-2">
                        {project.tags.map((tag) => (
                            <span
                                key={tag}
                                className="rounded-full border border-[#E7E2DA] bg-[#F8F7F4] px-3 py-1 text-xs font-medium text-[#1F2937]"
                            >
                                {tag}
                            </span>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    </Container>
    </FadeInSection>
    </section>
    );
}
