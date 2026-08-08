interface TimelineItemProps {
    title: string;
    organization: string;
    period: string;
    description: string;
}

export default function TimelineItem({
    title,
    organization,
    period,
    description,
}: TimelineItemProps) {
    return (
        <div className="relative pl-10">
            <div className="absolute left-0 top-2 h-4 w-4 rounded-full bg-[#C56E3D]" />
            <div className="absolute left-[7px] top-6 h-full w-px bg-[#E7E2DA]" />

            <div className="rounded-3xl border border-[#E7E2DA] bg-white p-6">
                <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                    <div>
                        <h3 className="text-xl font-semibold text-[#1F2937]">{title}</h3>
                        <p className="text-sm font-medium text-[#C56E3D]">{organization}</p>
                    </div>

                    <span className="text-sm text-[#6B7280]">{period}</span>
                </div>

                <p className="mt-4 text-base leading-relaxed text-[#6B7280]">
                    {description}
                </p>
            </div>
        </div>
    );
}
