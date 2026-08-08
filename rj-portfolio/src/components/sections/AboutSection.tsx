import Container from '@/components/common/Container';
import FadeInSection from '@/components/common/FadeInSection';

interface AboutSectionProps {
    dict: {
        subtitle: string;
        title: string;
        description: string;
    };
}

export default function AboutSection({ dict }: AboutSectionProps) {
    return (
        <section id="about" className="py-28">
            <FadeInSection>
                <Container>
                    <div className="grid gap-10 md:grid-cols-[1fr_1.5fr]">
                        <div>
                            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#C56E3D]">
                                {dict.subtitle}
                            </p>
                            <h2 className="mt-4 text-4xl font-bold text-[#1F2937] md:text-5xl">
                                {dict.title}
                            </h2>
                        </div>

                        <div>
                            <p className="text-lg leading-relaxed text-[#6B7280]">
                                {dict.description}
                            </p>
                        </div>
                    </div>
                </Container>
            </FadeInSection>
        </section>
    );
}
