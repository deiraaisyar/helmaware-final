import Container from '@/components/common/Container';
import FadeInSection from '@/components/common/FadeInSection';
import TimelineItem from '@/components/common/TimelineItem';

interface ExperienceSectionProps {
    locale: string;
    dict: {
        subtitle: string;
        title: string;
    };
}

export default function ExperienceSection({
    locale,
    dict,
}: ExperienceSectionProps) {
    const isID = locale === 'id';

    return (
        <section id="experience" className="py-28">
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

                    <div className="space-y-8">
                        <TimelineItem
                            title="CXQA Manager"
                            organization="AIESEC in UGM"
                            period="2025 – Present"
                            description={
                                isID
                                    ? 'Mengoordinasikan proses quality assurance, berkolaborasi dengan berbagai divisi, serta berkontribusi pada pelaksanaan proyek dan operasional organisasi.'
                                    : 'Coordinated quality assurance processes, collaborated with cross-functional teams, and contributed to project execution and organizational operations.'
                            }
                        />

                        <TimelineItem
                            title="Internal Affairs & Front-end Junior Staff"
                            organization="OmahTI"
                            period="2025 – Present"
                            description={
                                isID
                                    ? 'Mendukung operasional internal dan berkontribusi pada pengembangan front-end dalam ekosistem OmahTI.'
                                    : 'Supported internal operations and contributed to front-end development initiatives within the OmahTI ecosystem.'
                            }
                        />

                        <TimelineItem
                            title="IoT & AI Participant"
                            organization="Samsung Innovation Campus"
                            period="2025"
                            description={
                                isID
                                    ? 'Membangun proyek IoT dan AI menggunakan ESP32, MQTT, dan dasar-dasar machine learning dalam tim kolaboratif.'
                                    : 'Built IoT and AI projects using ESP32, MQTT, and machine learning fundamentals while working in collaborative technical teams.'
                            }
                        />

                        <TimelineItem
                            title="Research Assistant"
                            organization="RPLD Laboratory"
                            period="2025 – Present"
                            description={
                                isID
                                    ? 'Membantu kegiatan riset software engineering dan pengembangan teknis di lingkungan laboratorium.'
                                    : 'Assisted software engineering research activities and collaborated on technical development and experimentation within the laboratory environment.'
                            }
                        />
                    </div>
                </Container>
            </FadeInSection>
        </section>
    );
}
