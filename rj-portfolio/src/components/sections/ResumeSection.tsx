import Container from '@/components/common/Container';
import { Download } from 'lucide-react';
import FadeInSection from '@/components/common/FadeInSection';

export default function ResumeSection() {
    return (
        <section id="resume" className="bg-white py-28">
            <FadeInSection>
                <Container>
                    <div className="rounded-[2rem] border border-[#E7E2DA] bg-[#F8F7F4] p-10 md:p-14">
                        <div className="flex flex-col gap-8 md:flex-row md:items-center md:justify-between">
                            <div className="max-w-2xl">
                                <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#C56E3D]">
                                    Resume
                                </p>
                                <h2 className="mt-3 text-4xl font-bold text-[#1F2937] md:text-5xl">
                                    Download my resume.
                                </h2>
                                <p className="mt-4 text-lg leading-relaxed text-[#6B7280]">
                                    A concise overview of my education, technical experience,
                                    leadership roles, and selected software engineering projects.
                                </p>
                            </div>

                            <a
                                href="/resume/Regina_Joan_Resume_EN.pdf"
                                className="inline-flex items-center gap-2 rounded-full bg-[#1F2937] px-6 py-3 text-sm font-medium text-white transition hover:bg-[#111827]"
                            >
                                <Download size={18} />
                                Download CV
                            </a>
                        </div>
                    </div>
                </Container>
            </FadeInSection>
        </section>
    );
}