"use client"

import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import { Server, Database, Activity, Box } from "lucide-react"
import { cn } from "@/lib/utils"

type Resource = {
    id: string
    type: string
    status: "healthy" | "warning" | "critical"
    region: string
}

type InventoryData = {
    resources: Resource[]
}

const ResourceIcon = ({ type }: { type: string }) => {
    switch (type) {
        case "EC2": return <Server className="w-6 h-6" />
        case "RDS": return <Database className="w-6 h-6" />
        case "Lambda": return <Activity className="w-6 h-6" />
        default: return <Box className="w-6 h-6" />
    }
}

export function InventoryMap() {
    const [data, setData] = useState<InventoryData | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await fetch("http://localhost:8000/inventory")
                const json = await res.json()
                setData(json)
            } catch (error) {
                console.error("Failed to fetch inventory", error)
            } finally {
                setLoading(false)
            }
        }

        fetchData()
        const interval = setInterval(fetchData, 5000) // Poll every 5s
        return () => clearInterval(interval)
    }, [])

    if (loading) return <div className="text-primary animate-pulse">Scanning infrastructure...</div>

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data?.resources.map((res, i) => (
                <motion.div
                    key={res.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                    className={cn(
                        "p-6 rounded-xl border backdrop-blur-md transition-all duration-300",
                        res.status === "healthy" && "bg-green-500/10 border-green-500/30 hover:border-green-500",
                        res.status === "warning" && "bg-yellow-500/10 border-yellow-500/30 hover:border-yellow-500 animate-pulse",
                        res.status === "critical" && "bg-red-500/10 border-red-500/30 hover:border-red-500 animate-bounce"
                    )}
                >
                    <div className="flex items-center justify-between mb-4">
                        <div className={cn(
                            "p-2 rounded-lg",
                            res.status === "healthy" ? "bg-green-500/20 text-green-400" :
                                res.status === "warning" ? "bg-yellow-500/20 text-yellow-400" :
                                    "bg-red-500/20 text-red-400"
                        )}>
                            <ResourceIcon type={res.type} />
                        </div>
                        <span className="text-xs font-mono text-muted-foreground">{res.region}</span>
                    </div>

                    <h3 className="font-mono text-lg font-bold truncate" title={res.id}>{res.id}</h3>
                    <p className="text-sm text-gray-400 mt-1">{res.type} Resource</p>

                    <div className="mt-4 flex items-center gap-2">
                        <div className={cn(
                            "w-2 h-2 rounded-full",
                            res.status === "healthy" ? "bg-green-500" :
                                res.status === "warning" ? "bg-yellow-500" :
                                    "bg-red-500"
                        )} />
                        <span className="text-xs uppercase tracking-wider font-semibold">
                            {res.status}
                        </span>
                    </div>
                </motion.div>
            ))}
        </div>
    )
}
