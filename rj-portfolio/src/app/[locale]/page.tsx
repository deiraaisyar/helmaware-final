import HeroSection from '@/components/sections/HeroSection';
import AboutSection from '@/components/sections/AboutSection';
import ProjectsSection from '@/components/sections/ProjectsSection';
import ExperienceSection from '@/components/sections/ExperienceSection';
import SkillsSection from '@/components/sections/SkillsSection';
import ContactSection from '@/components/sections/ContactSection';
import { getDictionary } from '@/lib/getDictionary';
import NonITProjectsSection from '@/components/sections/NonITProjectsSection';

interface HomePageProps {
  params: Promise<{
    locale: string;
  }>;
}

export default async function HomePage({ params }: HomePageProps) {
  const { locale } = await params;
  const dict = await getDictionary(locale);

  return (<main className="bg-[#F8F7F4]"> <HeroSection locale={locale} dict={dict.hero} /> <AboutSection dict={dict.about} /> <ProjectsSection locale={locale} dict={dict.projects} /> <NonITProjectsSection locale={locale} /> <ExperienceSection locale={locale} dict={dict.experience} /> <SkillsSection locale={locale} dict={dict.skills} /> <ContactSection locale={locale} dict={dict.contact} /> </main>
  );
}
