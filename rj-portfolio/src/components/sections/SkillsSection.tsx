import Container from '@/components/common/Container';
import FadeInSection from '@/components/common/FadeInSection';

interface SkillsSectionProps {
    locale: string;
    dict: {
        subtitle: string;
        title: string;
    };
}

export default function SkillsSection({ locale, dict }: SkillsSectionProps) {
    const technical = [
        'Python',
        'TypeScript',
        'Java',
        'C++',
        'Next.js',
        'React',
        'PostgreSQL',
        'Supabase',
        'Docker',
        'Git',
    ];

    const soft = locale === 'id'
        ? [
            'Kepemimpinan Tim',
            'Komunikasi',
            'Kolaborasi',
            'Manajemen Proyek',
            'Pemecahan Masalah',
        ]
        : [
            'Team Leadership',
            'Communication',
            'Collaboration',
            'Project Management',
            'Problem Solving',
        ];

    return (
        <section id="skills" className="bg-[#F8F7F4] py-28">
            <FadeInSection>
                <Container>
                    <div className="mb-14">
                        <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#C56E3D]">
                            {dict.subtitle}
                        </p>
                        <h2 className="mt-3 text-4xl font-bold text-[#1F2937] md:text-5xl">
                            {dict.title}
                        </h2>
                    </div>

                    <div className="grid gap-8 md:grid-cols-2">
                        <div className="rounded-3xl border border-[#E7E2DA] bg-white p-6">
                            <h3 className="text-xl font-semibold text-[#1F2937]">
                                {locale === 'id' ? 'Keahlian Teknis' : 'Technical Skills'}
                            </h3>
                            <div className="mt-4 flex flex-wrap gap-2">
                                {technical.map((skill) => (
                                    <span
                                        key={skill}
                                        className="rounded-full border border-[#E7E2DA] bg-[#F8F7F4] px-3 py-1 text-sm font-medium text-[#1F2937]"
                                    >
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        </div>

                        <div className="rounded-3xl border border-[#E7E2DA] bg-white p-6">
                            <h3 className="text-xl font-semibold text-[#1F2937]">
                                {locale === 'id' ? 'Soft Skills' : 'Soft Skills'}
                            </h3>
                            <div className="mt-4 flex flex-wrap gap-2">
                                {soft.map((skill) => (
                                    <span
                                        key={skill}
                                        className="rounded-full border border-[#E7E2DA] bg-[#F8F7F4] px-3 py-1 text-sm font-medium text-[#1F2937]"
                                    >
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </div>
                </Container>
            </FadeInSection>
        </section>
    );
}
